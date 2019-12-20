def test_import_competancy_mgt():
    import competancy_mgt
    assert competancy_mgt is not None


def test_competancy_mgt_plugin_activation():
    from competancy_mgt.applications import COMPETANCY_MGT_APP
    from competancy_mgt.plugins.competancy_mgt_web_plugin import competancy_mgt_web_plugin

    my_app = COMPETANCY_MGT_APP()
    app = my_app.app
    app.plugins.activate(["competancy_mgt_plugin"])
    plugin = app.plugins.get("competancy_mgt_plugin")
    assert plugin is not None
    assert isinstance(plugin, competancy_mgt_web_plugin)
