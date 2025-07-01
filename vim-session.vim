let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Documents/clipclap/podcast_llama
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +1 ~/Documents/podcast_llama/src/audiogen/tts/tts_utils.py
badd +1 ~/Documents/podcast_llama/src/audiogen/models/__init__.py
badd +1 ~/Documents/podcast_llama/src/audiogen/tts/__init__.py
badd +1 ~/Documents/podcast_llama/src/audiogen/models/models.py
badd +1 ~/Documents/podcast_llama/src/audiogen/tts/tts.py
badd +1 neo-tree\ filesystem\ \[2]
badd +133 ~/Documents/clipclap/podcast_llama/src/audiogen/tts/tts_utils.py
badd +1 ~/Documents/clipclap/podcast_llama/src/audiogen/tts/tts.py
badd +1 ~/Documents/clipclap/podcast_llama/src/audiogen/tts/__init__.py
badd +1 ~/Documents/clipclap/podcast_llama/src/audiogen/models/models.py
badd +9 ~/Documents/clipclap/podcast_llama/src/audiogen/models/__init__.py
argglobal
%argdel
set stal=2
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit ~/Documents/clipclap/podcast_llama/src/audiogen/tts/tts_utils.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
wincmd =
argglobal
balt ~/Documents/podcast_llama/src/audiogen/tts/tts_utils.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 11,16fold
sil! 20,22fold
sil! 25,27fold
sil! 33,40fold
sil! 43,45fold
sil! 50,51fold
sil! 48,52fold
sil! 55,56fold
sil! 54,62fold
sil! 64,72fold
sil! 75,76fold
sil! 92,99fold
sil! 91,100fold
sil! 73,103fold
sil! 30,103fold
sil! 105,107fold
sil! 113,114fold
sil! 108,116fold
sil! 119,126fold
sil! 129,130fold
sil! 131,132fold
sil! 138,139fold
sil! 137,140fold
sil! 142,143fold
sil! 145,148fold
sil! 149,152fold
sil! 144,152fold
sil! 141,152fold
sil! 127,159fold
let &fdl = &fdl
let s:l = 133 - ((28 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 133
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/clipclap/podcast_llama/src/audiogen/tts/__init__.py", ":p")) | buffer ~/Documents/clipclap/podcast_llama/src/audiogen/tts/__init__.py | else | edit ~/Documents/clipclap/podcast_llama/src/audiogen/tts/__init__.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/clipclap/podcast_llama/src/audiogen/tts/__init__.py
endif
balt ~/Documents/podcast_llama/src/audiogen/tts/__init__.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 1,2fold
sil! 4,9fold
sil! 12,18fold
let &fdl = &fdl
let s:l = 13
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 13
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/clipclap/podcast_llama/src/audiogen/tts/tts.py", ":p")) | buffer ~/Documents/clipclap/podcast_llama/src/audiogen/tts/tts.py | else | edit ~/Documents/clipclap/podcast_llama/src/audiogen/tts/tts.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/clipclap/podcast_llama/src/audiogen/tts/tts.py
endif
balt ~/Documents/podcast_llama/src/audiogen/tts/tts.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 1,6fold
sil! 13,24fold
sil! 29,35fold
sil! 41,47fold
sil! 53,54fold
sil! 52,55fold
sil! 51,56fold
sil! 59,60fold
sil! 58,61fold
sil! 57,62fold
sil! 25,62fold
sil! 64,66fold
sil! 68,76fold
sil! 83,84fold
sil! 87,88fold
sil! 97,104fold
sil! 92,105fold
sil! 106,107fold
sil! 91,109fold
sil! 77,111fold
sil! 113,117fold
sil! 122,125fold
sil! 127,128fold
sil! 134,135fold
sil! 136,137fold
sil! 139,142fold
sil! 143,144fold
sil! 118,144fold
sil! 150,153fold
sil! 148,154fold
sil! 156,159fold
sil! 155,160fold
sil! 146,160fold
sil! 12,160fold
let &fdl = &fdl
let s:l = 1 - ((0 * winheight(0) + 20) / 41)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 0
wincmd w
wincmd =
tabnext
edit ~/Documents/clipclap/podcast_llama/src/audiogen/models/models.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
wincmd =
argglobal
balt ~/Documents/podcast_llama/src/audiogen/models/models.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 9,13fold
sil! 20,22fold
sil! 25,27fold
sil! 31,33fold
sil! 16,33fold
sil! 36,40fold
sil! 43,44fold
sil! 42,45fold
sil! 54,57fold
sil! 49,58fold
sil! 48,58fold
sil! 47,58fold
sil! 61,64fold
sil! 60,64fold
sil! 67,68fold
sil! 72,73fold
sil! 71,74fold
sil! 35,74fold
sil! 77,80fold
sil! 84,87fold
sil! 83,87fold
sil! 82,87fold
sil! 89,90fold
sil! 93,94fold
sil! 98,99fold
sil! 97,100fold
sil! 76,100fold
sil! 111,112fold
sil! 110,113fold
sil! 117,120fold
sil! 116,123fold
sil! 115,123fold
sil! 127,128fold
sil! 125,129fold
sil! 135,140fold
sil! 144,149fold
sil! 141,149fold
sil! 131,151fold
sil! 155,156fold
sil! 153,157fold
sil! 160,163fold
sil! 168,169fold
sil! 167,169fold
sil! 165,169fold
sil! 173,174fold
sil! 171,174fold
sil! 183,185fold
sil! 182,186fold
sil! 180,186fold
sil! 189,191fold
sil! 188,192fold
sil! 177,194fold
sil! 104,194fold
let &fdl = &fdl
let s:l = 8 - ((7 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 8
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/clipclap/podcast_llama/src/audiogen/models/__init__.py", ":p")) | buffer ~/Documents/clipclap/podcast_llama/src/audiogen/models/__init__.py | else | edit ~/Documents/clipclap/podcast_llama/src/audiogen/models/__init__.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/clipclap/podcast_llama/src/audiogen/models/__init__.py
endif
balt ~/Documents/podcast_llama/src/audiogen/models/__init__.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 1,5fold
sil! 10,15fold
let &fdl = &fdl
let s:l = 9 - ((8 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 9
normal! 0
wincmd w
wincmd =
tabnext 1
set stal=1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
