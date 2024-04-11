from vtt_to_srt.vtt_to_srt import ConvertFile


path = 'data\\我的超能力每周刷新\\6\\content.vtt'
convert_file = ConvertFile(path, "utf-8")
convert_file.convert()