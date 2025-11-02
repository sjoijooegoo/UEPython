import unreal

def get_all_actor(use_selection = False, actor_class = None, actor_tag = None):
    if use_selection:
        selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        if actor_class:
            selected_actors = [x for x in selected_actors if actor_class == x.get_class()]
        if actor_tag:
            selected_actors = [x for x in selected_actors if x.actor_has_tag(actor_tag)]
        return selected_actors
    else:
        world = unreal.EditorLevelLibrary.get_editor_world()
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class)
        if actor_tag:
            actors = [x for x in actors if x.actor_has_tag(actor_tag)]
        return actors

def print_actors(actor_class_path):
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class(actor_class_path)
    actors = get_all_actor(use_selection=False, actor_class=actor_class, actor_tag=None)
    for i in actors:
        print(i)

def select_actors(actor_to_select = []):
    unreal.EditorLevelLibrary.set_selected_level_actors(actor_to_select)

def test_select_actors(actor_class_path):
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class(actor_class_path)
    actors = get_all_actor(use_selection=False, actor_class=actor_class, actor_tag=None)
    select_actors(actor_to_select=actors)