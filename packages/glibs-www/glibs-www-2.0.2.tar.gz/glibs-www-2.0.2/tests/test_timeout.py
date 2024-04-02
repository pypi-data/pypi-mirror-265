import gevent
import pytest
import sys
import time
import webtest

from glibs.www import timeout


class AnotherException(Exception):
    pass


def pyramid_app():
    pyramid = pytest.importorskip("pyramid")

    config = pyramid.config.Configurator()
    config.registry.settings["gevent_timeout"] = "1"
    config.registry.settings["custom_timeout_by_endpoint"] = {
        "/test/custom/timeout/ok": 48
    }

    def view(request):
        if request.matchdict.get("op") == "timeout":
            gevent.sleep(40)
        elif request.matchdict.get("op") == "exception":
            raise AnotherException
        elif request.matchdict.get("op") == "python-timeout":
            now = time.time()
            while time.time() - now < 1.1:
                pass
        return "ok"

    def viewCustomTimeout(request):
        if request.matchdict.get("op") == "ok":
            gevent.sleep(40)
        elif request.matchdict.get("op") == "timeout":
            gevent.sleep(48)
        return "ok"

    config.add_route("test route", pattern="/test/{op}")
    config.add_route("test custom timeout route", pattern="/test/custom/timeout/{op}")
    config.add_view(view, route_name="test route", renderer="string")
    config.add_view(
        viewCustomTimeout, route_name="test custom timeout route", renderer="string"
    )

    timeout.bind_pyramid(config)

    return webtest.TestApp(config.make_wsgi_app())


def flask_app():
    flask = pytest.importorskip("flask")

    app = flask.Flask(__name__)
    app.config["gevent_timeout"] = "1"
    app.testing = True

    @app.route("/test/<op>")
    def view(op):
        if op == "timeout":
            gevent.sleep(40)
        elif op == "exception":
            raise AnotherException()
        elif op == "python-timeout":
            now = time.time()
            while time.time() - now < 1.1:
                pass
        return "ok"

    @app.route("/test/custom/timeout/<op>")
    def viewCustomTimeout(op):
        if op == "ok":
            return "ok"
        elif op == "timeout":
            now = time.time()
            while time.time() - now < 1.1:
                pass
        return "ok"

    timeout.bind_flask(app)

    return webtest.TestApp(app)


@pytest.fixture(params=[flask_app, pyramid_app])
def app(request):
    return request.param()


def test_ok(app):
    response = app.get("/test/ok")
    assert response.status_code == 200


def test_ok_with_custom_timeout(app):
    response = app.get("/test/custom/timeout/ok")
    assert response.status_code == 200


def test_timeout_on_gevent(app):
    with pytest.raises(timeout.DeadlineExceededError):
        app.get("/test/timeout")


def test_timeout_on_custom_timeout(app):
    with pytest.raises(timeout.DeadlineExceededError):
        app.get("/test/custom/timeout/timeout")


def test_timeout_on_python(app):
    with pytest.raises(timeout.DeadlineExceededError):
        app.get("/test/python-timeout")


def test_timeout_on_python_and_no_module_gevent(app, monkeypatch):
    monkeypatch.setitem(sys.modules, "gevent", None)
    with pytest.raises(timeout.DeadlineExceededError):
        app.get("/test/python-timeout")


def test_keeps_exception(app):
    with pytest.raises(AnotherException):
        app.get("/test/exception")
