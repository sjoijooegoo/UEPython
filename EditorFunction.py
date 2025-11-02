import unreal
import random
import AssetFunction

def deferredSpawnActor():
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/Blueprint/BP_Actor')
    actor_location = unreal.Vector(random.uniform(0, 2000), random.uniform(0, 2000), 0)
    actor_rotation = unreal.Rotator(random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360))
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, actor_location, actor_rotation)
    actor.tags.append('sdsdsdsd')
    return actor

def executeSlowTask():
    quantity_step_in_slow_task = 1000
    with unreal.ScopedSlowTask(quantity_step_in_slow_task, 'My Slow Task Text ..') as slow_task:
        slow_task.make_dialog(True)
        for x in range(quantity_step_in_slow_task):
            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1,'My Slow Task Text ...' + str(x) + '/' + str(quantity_step_in_slow_task))
            deferredSpawnActor()

def getAllProperty(object_class):
    return unreal.MyActor.get_all_properties(object_class)

def printAllProperty():
    obj = unreal.Actor()
    object_class = obj.get_class()
    for x in getAllProperty(object_class):
        print(x + ' : ' + str(obj.get_editor_property(x)))

def execCmd():
    console_cmd = ['r.ScreenPercentage 1',
                   'r.Color.Max 1',
                   'stat fps',
                   'stat unit']
    for i in console_cmd:
        unreal.MyActor.execute_console_command(i)