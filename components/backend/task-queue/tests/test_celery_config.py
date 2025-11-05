from celery_config import create_celery_app


def test_create_celery_app_returns_app():
    app = create_celery_app(app_name="test-app")
    assert app.main == "test-app"
    assert isinstance(app.conf.broker_url, str)
