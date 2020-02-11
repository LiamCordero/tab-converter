from pydub import AudioSegment

class Sound():
    def __init__(self, blocks):
        notes=[
        ['E6','F6','F#6','G6','G#6','A6','A#6','B6','C7','C#7','D7','D#7','E7','F7','F#7','G7','G#7','A7','A#7','B7','C8','C#8','D8','D#8','E8'],
        ['B5','C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6','A#6','B6','C7','C#7','D7','D#7','E7','F7','F#7','G7','G#7','A7','A#7','B7'],
        ['G5','G#5','A5','A#5','B5','C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6','A#6','B6','C7','C#7','D7','D#7','E7','F7','F#7','G7'],
        ['D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5','C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6','A#6','B6','C7','C#7','D7'],
        ['A4','A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5','C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6'],
        ['E4','F4','F#4','G4','G#4','A4','A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5','C6','C#6','D6','D#6','E6']
        ]
        for i in range(len(notes)):
            for j in range(len(notes[i])):
                notes[i][j]='notes/'+notes[i][j]+'.WAV'
        #Milliseconds Per Index
        mpi=50

        main=AudioSegment.empty()
        soundblocks=[]
        for i in range(len(blocks)):
            soundblocks.append([])
            for j in range(len(blocks[0])):
                soundblocks[i].append([])
                for k in range(len(blocks[i][0])):
                    if(blocks[i][j][k].isdigit()):
                        soundblocks[i][j].append(int(blocks[i][j][k]))
                    else:
                        soundblocks[i][j].append(-1)

        current=[]
        count=mpi
        for i in range(len(soundblocks)):
            for j in range(len(soundblocks[i][0])):
                new=AudioSegment.silent(duration=mpi)
                empty=True

                for string in range(len(soundblocks[i])):
                    fret=soundblocks[i][string][j]

                    if(soundblocks[i][string][j]>-1):
                        if(empty):
                            current=[]
                            empty=False
                        if(j!=len(soundblocks[i][string])-1):
                            next=soundblocks[i][string][j+1]
                            if(next>-1):
                                fret=int(str(fret)+str(next))
                                soundblocks[i][string][j+1]=-1


                        add=AudioSegment.from_wav(notes[string][fret])
                        new=new.overlay(add)
                        current.append(notes[string][fret])

                if(empty and len(main)!=0):
                    for note in current:
                        add=AudioSegment.from_wav(note)
                        new=new.overlay(add[count:mpi+count])
                    count+=mpi

                else:
                    count=mpi
                main=main.append(new,crossfade=0)
        r=main.export('tab.wav',format='wav')
