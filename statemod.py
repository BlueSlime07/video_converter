from pathlib import Path
import shutil
import pickle as pk

from functions import *

def state_read(state_file:Path,
               state_file_temp:Path,
               ) -> dict:
    if state_file_temp.exists():
        shutil.copy2(state_file_temp, state_file)
    with state_file.open('rb') as file:
        state = pk.load(file)
    return state


def state_write(state:dict,
                state_file:Path,
                state_file_temp:Path,
                ) -> None:
    with state_file_temp.open('wb') as file:
        pk.dump(state,file)
        file.close()
    shutil.copy2(state_file_temp, state_file)
    state_file_temp.unlink()

def make_default(state:dict,
                 input_dir:Path,
                 output_dir:Path,
                 videos:list[Path],
                 other_files:list[Path],
                 )->None:

        state["state_version"]=1
        state["input_directory"]=input_dir
        state["output_directory"]=output_dir
        state["input_videos"]=dict()
        for i in videos:
            state["input_videos"][i.relative_to(input_dir)] = get_file_hash(i)
        state["input_others"]=dict()
        for i in other_files:
            state["input_others"][i.relative_to(input_dir)] = get_file_hash(i)
        state["output_videos"]=[]
        state["output_others"]=[]
        state["encode_failed"]=[]
        state["copy_failed"]=[]

def merg_whit_scan(state:dict[str:dict[Path:str]],
                   state_file:Path,
                state_file_temp:Path,
                input_dir:Path,
                output_dir:Path,
                videos:list[Path],
                other_files:list[Path],
                
                   ) -> None:
    state["input_directory"]=input_dir
    state["output_directory"]=output_dir
    for_del_in_videos:list[Path]=[]
    for_del_in_others:list[Path]=[]
    for_del_in_videos_history:list[Path]=[]
    for_del_in_others_history:list[Path]=[]

    for video in state["input_videos"].keys():
        if not input_dir/video in videos:
            for_del_in_videos_history.append(video)
    
    for file in state["input_others"].keys():
        if not input_dir/file in other_files:
            for_del_in_others_history.append(file)
    
    for video in for_del_in_videos_history:
        try:state["output_videos"].remove(video)
        except:continue
    
    for file in for_del_in_others_history:
        try:state["output_others"].remove(file)
        except:continue

    for video in videos:
        if not video.relative_to(input_dir) in state["input_videos"].keys():
            state["input_videos"][video.relative_to(input_dir)] = get_file_hash(video)
        else:
            file_hash = get_file_hash(video)
            if ((state["input_videos"][video.relative_to(input_dir)] == file_hash) if not flag_control.IN_PLACE else True) and (video.relative_to(input_dir) in state["output_videos"]):
                for_del_in_videos.append(video)
            else:
                state["input_videos"][video.relative_to(input_dir)] = file_hash
                continue
    
    for file in other_files:
        if not file.relative_to(input_dir) in state["input_others"].keys():
            state["input_others"][file.relative_to(input_dir)] = get_file_hash(file)
        else:
            file_hash = get_file_hash(file)
            if state["input_others"][file.relative_to(input_dir)] == file_hash and file.relative_to(input_dir) in state["output_others"]:
                for_del_in_others.append(file)
            else:
                state["input_others"][file.relative_to(input_dir)] = file_hash
                continue
    del_in_list(videos,for_del_in_videos)
    del_in_list(other_files,for_del_in_others)
    state_write(state,state_file,state_file_temp)

def state_refresh(state_file:Path,
                  state_file_temp:Path,
                  input_dir:Path,
                  )->dict:
    state:dict[str:dict] = state_read(state_file,state_file_temp)
    
    state["state_version"]=1
    state["input_directory"]=input_dir
    state["output_directory"]= create_output_directory(input_dir)

    files = scan_files(input_dir)
    videos:list[Path] = []
    others:list[Path] = []
    split_files(files,videos,others)
    for_del:list[Path]=[]

    for file in state["input_videos"].keys():
        if not input_dir/file in videos:
            for_del.append(file)
    
    for file in for_del:
        state["input_videos"].pop(file)
    for_del.clear()

    for file in state["input_others"].keys():
        if not input_dir/file in others:
            for_del.append(file)
    
    for file in for_del:
        state["input_others"].pop(file)
    for_del.clear()
    files.clear()
    videos.clear()
    others.clear()

    files = scan_files(state["output_directory"])
    split_files(files,videos,others)

    for file in state["output_videos"]:
        if not(state["output_directory"]/file in videos or state["output_directory"]/file.with_suffix(".mkv") in videos):
            for_del.append(file)
    
    for file in for_del:
        state["output_videos"].remove(file)
    for_del.clear()
    
    for file in state["output_others"]:
        if not state["output_directory"]/file in others:
            for_del.append(file)
    
    for file in for_del:
        state["output_others"].remove(file)
    
    state_write(state,state_file,state_file_temp)
    