import pandas as pd
import os

# -*- coding: utf-8 -*-
# print(os.getcwd)


def arrange_songs(base_path, list_songs) -> dict:
    song_dict = dict()
    for song in list_songs:
        song_path = base_path + "/" + song
        with open(song_path, mode="r", encoding="utf-8") as file:
            song_text = file.read()

        beginverse_pos = song_text.find("\\beginverse")

        song_name = song_text[song_text.find("{") + 1 : song_text.find("}")]
        song_name = song_name.title()
        # print(song_name)

        song_text = (
            song_text[: song_text.find("{") + 1]
            + song_name.title()
            + song_text[song_text.find("}") :]
        )

        song_modified = (
            song_text[:beginverse_pos]
            + f"\phantomsection  \\addcontentsline{'{toc}{section}'}{ '{'+ song_name+ '}' } \n \label{'{sec:'+song_name.replace(' ','_')+'}'} "
            + song_text[beginverse_pos:]
        )

        song_dict[song_name] = song_modified
    return song_dict


def build_text_for_tex(folder_songs_dict: dict) -> str:
    text = "\n \n"
    for song in folder_songs_dict.keys():
        text += folder_songs_dict[song] + "\n \n"
    return text


folders = os.listdir("generos")


for folder in folders:
    folder_path = "generos/" + folder
    songs = os.listdir(folder_path)
    print(songs)

    folder_songs_dict = arrange_songs(folder_path, songs)
    sorted_dict = dict(sorted(folder_songs_dict.items(), key=lambda x: x[0]))
    text_for_tex = build_text_for_tex(sorted_dict)
    with open(f"{folder}.tex", "w", encoding="utf-8") as file:
        file.write(text_for_tex)
