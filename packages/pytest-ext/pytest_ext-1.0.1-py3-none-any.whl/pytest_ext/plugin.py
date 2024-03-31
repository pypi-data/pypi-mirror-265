import os
import time
import datetime
from pathlib import Path
import json
import logging
import shutil
import subprocess
import tempfile
import pytest
from pytest import ExitCode
import allure
from allure_pytest import utils as allure_utils
from pytest_ext.libs.helper import load_yaml
try:
    from pytest_ext.ui_libs.element_ext import (
        local_driver,
        remote_driver
    )
    from pytest_ext.ui_libs.basicelement import BasicElement
    IS_UI_TEST = True
except Exception:
    IS_UI_TEST = False

logger = logging.getLogger()
BROWSER = ['Chrome']


def pytest_addoption(parser):
    if IS_UI_TEST:
        parser.addoption('--sel-server', action='store',
                         help='指定selenium server IP和端口，如： 127.0.0.1:4444')
        parser.addoption("--browser", action="append", default=list(), help="指定浏览器")
    parser.addoption('--allure-report-url', action='store',
                     help='指定Allure报告的URL, 如在Jenkins执行自动化, 启动命令加上此参数：--allure-report-url=${JENKINS_URL}job/${JOB_NAME}/${BUILD_NUMBER}/allure/')
    parser.addoption("--auto-generate-report", action="store_true", help="是否自动生成allure报告")


if IS_UI_TEST:
    def pytest_generate_tests(metafunc):
        if "browser" in metafunc.fixturenames:
            metafunc.parametrize("browser", metafunc.config.getoption("browser") or BROWSER, indirect=True)


    @pytest.fixture(scope="session")
    def browser(request):
        return request.param


    @pytest.fixture(scope="session")
    def driver(request, browser):
        sel_svr = request.config.getoption('--sel-server')
        if sel_svr:
            driver = remote_driver(svr=sel_svr, browser=browser)
        else:
            driver = local_driver(browser=browser)
        driver.maximize_window()
        driver.implicitly_wait(5)
        # resolution = get_screen_resolution(driver)
        # logger.info(f'当前屏幕分辨率为width: {resolution["width"]}, height: {resolution["height"]}')
        pytest.driver = driver
        return driver


    @pytest.fixture(scope="session")
    def basic_element(driver):
        be = BasicElement(driver=driver)
        pytest.be = be
        return be


    @pytest.fixture(scope="session")
    def setup(request, driver, basic_element, shared_data):
        pytest.ts_data = dict()
        # pytest.finish_notice = request.config.getoption('--finish-notice')
        for item in request.node.items:
            cls = item.getparent(pytest.Class)
            setattr(cls.obj, 'shared_data', shared_data)
            setattr(cls.obj, 'driver', driver)
            setattr(cls.obj, 'be', basic_element)
        yield
        driver.quit()
else:

    @pytest.fixture(scope="session")
    def setup(request, shared_data):
        pytest.ts_data = dict()
        # pytest.finish_notice = request.config.getoption('--finish-notice')
        for item in request.node.items:
            cls = item.getparent(pytest.Class)
            setattr(cls.obj, 'shared_data', shared_data)
        yield


@pytest.fixture(scope="session")
def shared_data(request):
    shared_data_fp = Path(request.config.rootdir / 'testsuite' / 'data')
    sdata = dict()
    if not shared_data_fp.exists():
        return sdata

    data_files = list(shared_data_fp.glob('*'))
    for f in data_files:
        sdata[f.stem] = load_yaml(fp=f)
    return sdata


@pytest.fixture(autouse=True)
def tmp(tmp_path):
    tmp_name = str(time.time())
    d = tmp_path / tmp_name
    d.mkdir()
    pytest.tmp_dir = d


#######################
# 测试报告
#######################


# 失败用例自动截图函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    失败用例自动截图函数
    :param item:
    :param call:
    :return:
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        if IS_UI_TEST:
            logger.info('校验失败，进行截图记录...')
            allure.attach(pytest.driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


# def gen_test_item_file(session, fp):
#     items_info = dict()
#     if getattr(session, 'items', None) is None:
#         return
#     for item in session.items:
#         items_info[item.nodeid] = dict()
#         items_info[item.nodeid]['display_name'] = allure_utils.allure_name(item=item, parameters=getattr(item, 'callspec',
#                                                                                    None) and item.callspec.params or {})
#         severity_list = allure_utils.allure_label(item=item, label='severity')
#         items_info[item.nodeid]['severity'] = severity_list and severity_list[0] or 'normal'
#         feature_list = allure_utils.allure_label(item=item, label='feature')
#         items_info[item.nodeid]['feature'] = feature_list and feature_list[0] or '其它'
#         items_info[item.nodeid]['location'] = item.location[0]
#     with open(fp, 'w') as f:
#         f.write(json.dumps(items_info))


def pytest_sessionstart(session):
    if os.environ.get("PYTEST_XDIST_WORKER", "master") == "master":
        session.config.start_time = datetime.datetime.now()


# def pytest_sessionfinish(session, exitstatus):
#     # 在子节点结束session时，将目录
#     report_dir = session.config.getoption('--alluredir') or tempfile.gettempdir()
#     test_item_info_dir = Path(report_dir) / datetime.datetime.strftime(session.config.start_time, '%Y%m%d_%H%M%S')
#     test_item_info_fp = test_item_info_dir / 'test_item_info.json'
#     Path.mkdir(test_item_info_dir)
#     open(test_item_info_fp, 'a').close()
#     gen_test_item_file(session, fp=test_item_info_fp)


def generate_allure_report(config):
    # 生成allure报告
    auto_gen_report = config.getoption('--auto-generate-report')
    report_dir = config.getoption('--alluredir')
    html_report_dir = Path(report_dir) / datetime.datetime.strftime(config.start_time, '%Y%m%d_%H%M%S')
    if auto_gen_report and report_dir is not None:
        cmd = f'allure generate {report_dir} -o {str(Path(html_report_dir))} --clean'
        subprocess.call(cmd.split())


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if os.environ.get("PYTEST_XDIST_WORKER", "master") == "master":
        generate_allure_report(config)
