import os
import musicbrainzngs as mb
from mutagen.easyid3 import EasyID3

# 初始化路径
init_path = r'E:\musi'
# 设置 MusicBrainz API 的用户代理
mb.auth("AeenMB", "..dtz..384")
mb.set_useragent("MusicTagger", "1.0", "https://musci.tag.com")


def get_musicbrainz_tags(filename):
    """
    根据文件名从 MusicBrainz API 获取音乐标签。
    """
    try:
        # 从文件名中提取艺术家和歌曲名
        artist, title = os.path.splitext(os.path.basename(filename))[0].split(' - ')
        # 调用 MusicBrainz API 搜索曲目
        result = mb.search_recordings(artist=artist, recording=title)
        # 假设我们取第一个搜索结果
        recording = result['recording-list'][0]
        # 获取标签信息
        tags = {
            'title': recording['title'],
            'artist': recording['artist-credit'][0]['artist']['name'],
            'album': recording['release-list'][0]['title'],
            'tracknumber': recording['release-list'][0]['medium-list'][0]['track-list'][0]['number'],
            'date': recording['release-list'][0]['date'],
        }
        return tags
    except Exception as e:
        print(f"Error fetching tags for {filename}: {e}")
        return None

def update_tags(filename, tags):
    """
    使用 mutagen 更新音乐文件的标签。
    """
    try:
        audio = EasyID3(filename)
        for tag, value in tags.items():
            audio[tag] = value
        audio.save()
        print(f"Updated tags for {filename}")
    except Exception as e:
        print(f"Error updating tags for {filename}: {e}")

def main():
    # 遍历 E:\musi 目录中的所有文件
    for root, dirs, files in os.walk(init_path):
        for file in files:
            if file.endswith(('.mp3', '.flac', '.ogg')):  # 只处理常见的音乐文件格式
                filename = os.path.join(root, file)
                # print(filename)
                tags = get_musicbrainz_tags(filename)
                print(tags)
                # if tags:
                #     update_tags(filename, tags)

if __name__ == "__main__":
    main()