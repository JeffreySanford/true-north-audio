import os
import fluidsynth

# Path to your MIDI file
midi_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'src', 'assets', 'generated', 'liberty_blues_COUNTRY_BAND.mid')
# Path to output WAV file
wav_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'src', 'assets', 'generated', 'liberty_blues_COUNTRY_BAND.wav')
# Path to your soundfont (download FluidR3_GM.sf2 and place here)
sf2_path = os.path.join(os.path.dirname(__file__), 'FluidR3_GM.sf2')

if not os.path.exists(sf2_path):
    print("❌ Soundfont not found! Please download FluidR3_GM.sf2 and place it in ai_music_gen directory.")
    print("Download: https://member.keymusician.com/Member/FluidR3_GM/index.html or search for 'FluidR3_GM.sf2'.")
    exit(1)

fs = fluidsynth.Synth()
fs.start(driver='file', filename=wav_path)
sfid = fs.sfload(sf2_path)
fs.program_select(0, sfid, 0, 0)
fs.midi_file_play(midi_path)
fs.delete()

print(f"✅ Rendered {midi_path} to {wav_path} using {sf2_path}")
