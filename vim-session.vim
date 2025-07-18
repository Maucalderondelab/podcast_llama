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
badd +1 neo-tree\ filesystem\ \[1]
badd +4 ~/Documents/clipclap/podcast_llama/src/audiogen/__init__.py
badd +121 ~/Documents/clipclap/podcast_llama/src/mediagen/models/model_manager.py
badd +6 ~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts.py
badd +1 ~/Documents/clipclap/podcast_llama/src/mediagen/models/zyphra_zonos.py
badd +1 ~/Documents/clipclap/podcast_llama/src/mediagen/models/sesame_csm.py
badd +13 ~/Documents/clipclap/podcast_llama/src/mediagen/models/__init__.py
badd +1 ~/Documents/clipclap/podcast_llama/src/mediagen/utils/utils.py
badd +6 ~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts_utils.py
badd +16 ~/Documents/clipclap/podcast_llama/src/mediagen/tts/__init__.py
badd +71 ~/Documents/clipclap/podcast_llama/src/mediagen/models/audio/zyphra_zonos.py
badd +3 ~/Documents/clipclap/podcast_llama/src/mediagen/models/audio/sesame_csm.py
badd +0 ~/Documents/clipclap/podcast_llama/src/mediagen/utils/__init__.py
argglobal
%argdel
set stal=2
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit ~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts.py
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
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 11,13fold
sil! 17,19fold
sil! 24,31fold
sil! 34,36fold
sil! 41,42fold
sil! 39,43fold
sil! 46,47fold
sil! 45,53fold
sil! 56,64fold
sil! 67,68fold
sil! 84,91fold
sil! 83,92fold
sil! 65,95fold
sil! 21,95fold
let &fdl = &fdl
21
sil! normal! zo
45
sil! normal! zo
let s:l = 57 - ((39 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 57
normal! 013|
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts_utils.py", ":p")) | buffer ~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts_utils.py | else | edit ~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts_utils.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts_utils.py
endif
balt ~/Documents/clipclap/podcast_llama/src/mediagen/tts/tts.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 8,12fold
sil! 16,18fold
sil! 25,26fold
sil! 21,27fold
sil! 31,33fold
sil! 39,40fold
sil! 34,42fold
sil! 47,54fold
sil! 57,58fold
sil! 59,60fold
sil! 66,67fold
sil! 65,68fold
sil! 70,71fold
sil! 73,76fold
sil! 77,80fold
sil! 72,80fold
sil! 69,80fold
sil! 55,87fold
let &fdl = &fdl
55
sil! normal! zo
65
sil! normal! zo
let s:l = 25 - ((24 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 25
normal! 08|
wincmd w
wincmd =
tabnext
edit ~/Documents/clipclap/podcast_llama/src/mediagen/models/model_manager.py
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
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 12,14fold
sil! 21,23fold
sil! 26,28fold
sil! 32,34fold
sil! 37,39fold
sil! 42,44fold
sil! 17,44fold
sil! 55,56fold
sil! 54,57fold
sil! 61,64fold
sil! 60,67fold
sil! 59,67fold
sil! 71,72fold
sil! 69,73fold
sil! 79,84fold
sil! 88,93fold
sil! 85,93fold
sil! 75,95fold
sil! 99,100fold
sil! 97,101fold
sil! 104,107fold
sil! 112,113fold
sil! 111,113fold
sil! 109,113fold
sil! 117,118fold
sil! 115,118fold
sil! 121,123fold
sil! 133,135fold
sil! 132,136fold
sil! 130,136fold
sil! 139,141fold
sil! 138,142fold
sil! 127,144fold
sil! 48,144fold
let &fdl = &fdl
48
sil! normal! zo
115
sil! normal! zo
115
sil! normal! zc
let s:l = 123 - ((21 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 123
normal! 035|
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/clipclap/podcast_llama/src/mediagen/models/__init__.py", ":p")) | buffer ~/Documents/clipclap/podcast_llama/src/mediagen/models/__init__.py | else | edit ~/Documents/clipclap/podcast_llama/src/mediagen/models/__init__.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/clipclap/podcast_llama/src/mediagen/models/__init__.py
endif
balt ~/Documents/clipclap/podcast_llama/src/mediagen/models/model_manager.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 7,12fold
let &fdl = &fdl
let s:l = 9 - ((8 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 9
normal! 0
wincmd w
wincmd =
tabnext
edit ~/Documents/clipclap/podcast_llama/src/mediagen/models/audio/sesame_csm.py
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
balt ~/Documents/clipclap/podcast_llama/src/mediagen/models/sesame_csm.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 8,9fold
sil! 13,16fold
sil! 21,24fold
sil! 20,24fold
sil! 19,24fold
sil! 27,28fold
sil! 31,32fold
sil! 36,37fold
sil! 35,38fold
sil! 12,38fold
let &fdl = &fdl
let s:l = 25 - ((24 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 25
normal! 04|
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/clipclap/podcast_llama/src/mediagen/models/audio/zyphra_zonos.py", ":p")) | buffer ~/Documents/clipclap/podcast_llama/src/mediagen/models/audio/zyphra_zonos.py | else | edit ~/Documents/clipclap/podcast_llama/src/mediagen/models/audio/zyphra_zonos.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/clipclap/podcast_llama/src/mediagen/models/audio/zyphra_zonos.py
endif
balt ~/Documents/clipclap/podcast_llama/src/mediagen/models/zyphra_zonos.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 13,14fold
sil! 18,22fold
sil! 25,26fold
sil! 24,27fold
sil! 39,41fold
sil! 38,42fold
sil! 32,43fold
sil! 31,43fold
sil! 30,43fold
sil! 47,50fold
sil! 46,50fold
sil! 54,55fold
sil! 59,60fold
sil! 58,61fold
sil! 73,74fold
sil! 71,75fold
sil! 78,79fold
sil! 77,85fold
sil! 64,86fold
sil! 89,99fold
sil! 17,99fold
let &fdl = &fdl
let s:l = 71 - ((10 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 71
normal! 013|
wincmd w
2wincmd w
wincmd =
tabnext
edit ~/Documents/clipclap/podcast_llama/src/mediagen/utils/utils.py
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
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 8,9fold
sil! 10,12fold
sil! 15,18fold
sil! 26,29fold
sil! 31,32fold
sil! 34,35fold
sil! 51,56fold
sil! 74,75fold
sil! 81,83fold
sil! 84,85fold
sil! 70,85fold
sil! 65,91fold
sil! 61,91fold
sil! 94,95fold
sil! 92,96fold
sil! 47,98fold
sil! 101,102fold
sil! 22,104fold
sil! 113,116fold
sil! 118,119fold
sil! 122,126fold
sil! 147,149fold
sil! 144,149fold
sil! 140,149fold
sil! 137,149fold
sil! 151,155fold
sil! 163,164fold
sil! 162,166fold
sil! 168,171fold
sil! 172,175fold
sil! 156,175fold
sil! 132,175fold
sil! 178,179fold
sil! 109,181fold
sil! 190,191fold
sil! 204,206fold
sil! 186,206fold
let &fdl = &fdl
let s:l = 1 - ((0 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("~/Documents/clipclap/podcast_llama/src/mediagen/utils/__init__.py", ":p")) | buffer ~/Documents/clipclap/podcast_llama/src/mediagen/utils/__init__.py | else | edit ~/Documents/clipclap/podcast_llama/src/mediagen/utils/__init__.py | endif
if &buftype ==# 'terminal'
  silent file ~/Documents/clipclap/podcast_llama/src/mediagen/utils/__init__.py
endif
balt ~/Documents/clipclap/podcast_llama/src/mediagen/utils/utils.py
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 1,4fold
sil! 7,10fold
let &fdl = &fdl
let s:l = 9 - ((8 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 9
normal! 0
wincmd w
wincmd =
tabnext
edit ~/Documents/clipclap/podcast_llama/src/mediagen/tts/__init__.py
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal foldmethod=manual
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
silent! normal! zE
sil! 5,7fold
sil! 10,14fold
sil! 17,24fold
let &fdl = &fdl
let s:l = 16 - ((15 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 16
normal! 0
tabnext 3
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
