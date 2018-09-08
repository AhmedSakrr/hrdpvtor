#!flask/bin/python

from flask import Flask,jsonify,request


app = Flask(__name__)


#LOAD THE MODEL_______________________________________________________________________________

import hparams
import json

# Newly added params. Need to inject dummy values
for dummy, v in [("fmin", 0), ("fmax", 0), ("rescaling", False),
                ("rescaling_max", 0.999), 
                ("allow_clipping_in_normalization", False)]:
                if hparams.hparams.get(dummy) is None:
                    hparams.hparams.add_hparam(dummy, v)
    
# Load parameters from preset
preset = "./presets/deepvoice3_vctk.json"
with open(preset) as f:
    hparams.hparams.parse_json(f.read())

# Tell we are using multi-speaker DeepVoice3
hparams.hparams.builder = "deepvoice3_multispeaker"

# Inject frontend text processor
import synthesis
import train
from deepvoice3_pytorch import frontend
synthesis._frontend = getattr(frontend, "en")
train._frontend =  getattr(frontend, "en")

# alises
fs = hparams.hparams.sample_rate
hop_length = hparams.hparams.hop_size
####
from train import build_model
from train import restore_parts, load_checkpoint

def tts(model, text, p=0, speaker_id=0, fast=True, figures=True):
    from synthesis import tts as _tts
    waveform, alignment, spectrogram, mel = _tts(model, text, p, speaker_id, fast)
    return waveform, alignment, spectrogram, mel

checkpoint_path = "20171222_deepvoice3_vctk108_checkpoint_step000300000.pth"
model = build_model()
model = load_checkpoint(checkpoint_path, model, None, True)
#____________________________________________________________________________

# Try your favorite senteneces:)

text = "Some have accepted this as a miracle without any physical explanation"
N = 15
print("Synthesizing \"{}\" with {} different speakers".format(text, N))
# for speaker_id in range(N):
#     print(speaker_id)
# tts(model, text, speaker_id=speaker_id, figures=False)


@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    return response

@app.route("/")
def hello():
    return "Welcome"






if __name__ == "__main__":
    app.run(debug=True)