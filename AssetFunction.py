import unreal

def print_ue_class_methods(class_name):
    """打印UE类中所有Python可调用的方法"""
    
    # 获取UClass
    uclass = unreal.__dict__.get(class_name)
    if uclass is None:
        print(f"未找到类: {class_name}")
        return
    
    print(f"UE类 {class_name} 中的可调用方法:")
    print("-" * 60)
    
    # 获取所有函数
    for attr_name in dir(uclass):
        attr = getattr(uclass, attr_name)
        if callable(attr):
            print(f"  {attr_name}")

def buildImportTask(fileName, destination_path, options = None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', fileName)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task

def executeImportTasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            print ('Imported: %s' % path)

def importSimpleAssets():
    texture_tag = 'C:/Users/Song/Desktop/Assets/T_Brick_Cut_Stone_D.PNG'
    sound_tag = 'C:/Users/Song/Desktop/Assets/Collapse01.WAV'

    texture_task = buildImportTask(texture_tag, '/Game/Textures')
    sound_task = buildImportTask(sound_tag, '/Game/Sounds')
    executeImportTasks([texture_task, sound_task])

def importMeshAssets():
    staticMesh_source = 'C:/Users/Song/Desktop/Assets/SM_Chair.FBX'
    skeletalMesh_source = 'C:/Users/Song/Desktop/Assets/SK_Mannequin.FBX'
    staticMesh_task = buildImportTask(staticMesh_source, '/Game/Mesh', buildStaticMeshOptions())
    skeletalMesh_task = buildImportTask(skeletalMesh_source, '/Game/Mesh', buildSkeletalMeshOptions())
    executeImportTasks([staticMesh_task, skeletalMesh_task])

def importAnimAssets():
    Anim_Source = 'C:/Users/Song/Desktop/Assets/Crouch_Walk_Fwd_Rifle_Hip.FBX'
    Skeleton_Source = '/Game/Mesh/SK_Mannequin_Skeleton'
    Anim_task = buildImportTask(Anim_Source, '/Game/Anim', buildAnimOptions(Skeleton_Source))
    executeImportTasks([Anim_task])

def buildAnimOptions(Skeleton_Path):
    options = unreal.FbxImportUI()
    options.set_editor_property('import_animations', True)
    options.set_editor_property('import_mesh', False)  # 不导入网格
    options.set_editor_property('import_as_skeletal', False)  # 不作为骨骼网格导入
    options.automated_import_should_detect_type = False
    skeleton = unreal.load_asset(Skeleton_Path)
    if skeleton:
        options.skeleton = skeleton
        unreal.log("骨架加载成功")
    else:
        unreal.log_error(f"无法加载骨架: {Skeleton_Path}")
    # options.anim_sequence_import_data.set_editor_property('import_translation', unreal.Vector(0, 0, 0))
    # options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Rotator(0, 0.0, 0))
    # options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)
    # options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    # options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', False)
    return options

def buildStaticMeshOptions():
    options = unreal.FbxImportUI()
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', False)
    
    options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(50, 0, 0))
    options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0, 110.0, 0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    
    options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
    return options

def buildSkeletalMeshOptions():
    options = unreal.FbxImportUI()
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', True)
    
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0, 0, 0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0, 110.0, 0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    return options

def saveAsset(path = '', force_save = True):
    return unreal.EditorAssetLibrary.save_asset(asset_to_save = path, only_if_is_dirty= not force_save)

def directoryExist():
    new_dir = '/Game/ExistDir'
    print (unreal.EditorAssetLibrary.does_directory_exist(new_dir))
    print (unreal.EditorAssetLibrary.does_directory_exist(new_dir + 'Duplicated'))

def createDirectory():
    unreal.EditorAssetLibrary.make_directory('/Game/ExistDir')

def callCPP():
    unreal.MyActor.call_from_python('/Game/Mesh')

def duplicatedAsset(show_dialog : bool = True):
    asset_source = '/Game/Mesh/SM_Chair'
    splitedPath = asset_source.rsplit('/', 1)
    asset_dir = splitedPath[0]
    duplicated_asset_name = splitedPath[1] + '_dup'
    if show_dialog :
        return unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset_with_dialog(asset_name = duplicated_asset_name, package_path = asset_dir, original_object = unreal.load_asset(asset_source))
    else:
        return unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name = duplicated_asset_name, package_path = asset_dir, original_object = unreal.load_asset(asset_source))

def openAssets():
    assets = [unreal.load_asset('/Game/Mesh/SM_Chair')]  
    unreal.AssetToolsHelpers.get_asset_tools().open_editor_for_assets(assets) 

def closeAssets():
    assets = unreal.MyActor.get_assets_opened_in_editor()
    unreal.MyActor.close_editor_for_assets(assets)

def showAssetsInContentBrowser():
    paths = ['/Game/Mesh/SM_Chair',
             '/Game/Mesh/SK_Mannequin_Skeleton']
    unreal.EditorAssetLibrary.sync_browser_to_objects(paths)

def openSelectAssets():
    assetPaths = unreal.MyActor.get_selected_assets()
    assets = []
    for path in assetPaths:
        assets.append(unreal.load_asset(path))
    unreal.AssetToolsHelpers.get_asset_tools().open_editor_for_assets(assets) 

def create_generic_asset(asset_path = '', unique_name=True, asset_class=None, asset_factory=None):
    package_name, asset_name = unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(
        base_package_name = asset_path,
        suffix = ''
    )
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path = package_name):
        path = package_name.rsplit('/', 1)[0]
        name = package_name.rsplit('/', 1)[1]
        return unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name=name,
            package_path=path,
            asset_class=asset_class,
            factory=asset_factory
        )
    return unreal.load_asset(asset_path)

def create_generic_asset_TEST():
    base_path = '/Game/GenericAsset'
    generic_assets = [
        [
            base_path+'/sequence',
            unreal.LevelSequence,
            unreal.LevelSequenceFactoryNew()
        ],
        [
            base_path+'/material',
            unreal.Material,
            unreal.MaterialFactoryNew()
        ]
    ]
    for i in generic_assets:
        create_generic_asset(asset_path=i[0], unique_name=True, asset_class=i[1], asset_factory=i[2])
