import subprocess
import os
from os.path import exists, join, expanduser

if __name__ == "__main__":
    #nltk.download('popular', halt_on_error=False)
    checkpoint_path = "20171222_deepvoice3_vctk108_checkpoint_step000300000.pth"
    if not exists(checkpoint_path):
        subprocess.call('curl -O -L "https://www.dropbox.com/s/uzmtzgcedyu531k/20171222_deepvoice3_vctk108_checkpoint_step000300000.pth"'
        ,shell=True)
    preset = "./presets/deepvoice3_vctk.json"
    subprocess.call("cp -v {preset} .".format(preset) ,shell=True)
    subprocess.call("pip install -q -e '.[train]'",shell=True)
    #subprocess.call("python -m nltk.downloader cmudict",shell=True)


