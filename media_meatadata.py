from pprint import pprint
from pymediainfo import MediaInfo
def metadatainfo(samplefile):
    samplefile_real=(str(samplefile))
    media_info = MediaInfo.parse(samplefile_real)
    res=[]
    for track in media_info.tracks:
        track = track.to_data()
        res.append(track)
    return res
        # if track.track_type == "Video":
        #     print(track)
        #     print("Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "
        #           "Format: {t.format}".format(t=track)
        #     )
        #     print("Duration (raw value):", track.duration)
        #     print("Duration (other values:")
        #     pprint(track.other_duration)
        # elif track.track_type == "Audio":
        #     print("Track data:")
        #     pprint(track.to_data())