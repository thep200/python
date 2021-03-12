" Nvim setup file by Thep200

call plug#begin('~/AppData/Local/nvim/plugged')

Plug 'mhinz/vim-startify', {'branch': 'center'}
Plug 'joshdick/onedark.vim'
Plug 'preservim/NERDTree'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'itchyny/lightline.vim'
Plug 'jiangmiao/auto-pairs'
Plug 'dense-analysis/ale'
Plug 'davidhalter/jedi-vim'

call plug#end()


" Setup Plugin
	" CtrP
		if executable('rg')
		  let g:ctrlp_user_command = 'rg %s --files --hidden --color=never --glob ""'
		endif
		
		set wildignore+=*\\tmp\\*,*.swp,*.zip,*.exe  " Windows
		let g:ctrlp_custom_ignore = '\v[\/]\.(git|hg|svn)$'
		let g:ctrlp_custom_ignore = {
		  \ 'dir':  '\v[\/]\.(git|hg|svn)$',
		  \ 'file': '\v\.(exe|so|dll)$',
		  \ 'link': 'some_bad_symbolic_links',
		  \ }

	" Ale
		let g:ale_sign_error = '✘'
		let g:ale_sign_warning = '✗'

	" Screen Startup
		let g:startify_bookmarks = systemlist("cut -sd' ' -f 5- ~/.NERDTreeBookmarks")

	" Jedi-vim setup
		let g:pymode_rope = 0
		let g:jedi#popup_select_first = 0
		autocmd FileType python setlocal completeopt-=preview

	"Basic
		set number
		set encoding=utf-8
		set fileencodings=utf-8

	" NERDTree
		map <C-a> :NERDTreeToggle<CR> 
		map <C-s> :NERDTreeFind<CR> 
		set autochdir
		let NERDTreeChDirMode=2
		let NERDTreeMinimalUI=1
		autocmd BufEnter * if bufname('#') =~ 'NERD_tree_\d\+' && bufname('%') !~ 'NERD_tree_\d\+' && winnr('$') > 1 |
			\ let buf=bufnr() | buffer# | execute "normal! \<C-W>w" | execute 'buffer'.buf | endif
		autocmd BufWinEnter * silent NERDTreeMirror
		let g:NERDTreeDirArrowExpandable = '▸'
		let g:NERDTreeDirArrowCollapsible = '▾'

	" Themes
		colorscheme onedark

	" Lightline
		let g:lightline = { 'colorscheme': 'onedark' }

" Setup Basic
	"Always show tabs
		set showtabline=2

	" Floating Windows Terminal
		function! OpenFloatTerm()
		  let height = float2nr((&lines - 2) / 1.5)
		  let row = float2nr((&lines - height) / 2)
		  let width = float2nr(&columns / 1.5)
		  let col = float2nr((&columns - width) / 2)
		  let border_opts = {
			\ 'relative': 'editor',
			\ 'row': row - 1,
			\ 'col': col - 2,
			\ 'width': width + 4,
			\ 'height': height + 2,
			\ 'style': 'minimal'
			\ }
		  let border_buf = nvim_create_buf(v:false, v:true)
		  let s:border_win = nvim_open_win(border_buf, v:true, border_opts)
		  let opts = {
			\ 'relative': 'editor',
			\ 'row': row,
			\ 'col': col,
			\ 'width': width,
			\ 'height': height,
			\ 'style': 'minimal'
			\ }
		  let buf = nvim_create_buf(v:false, v:true)
		  let win = nvim_open_win(buf, v:true, opts)
		  terminal
		  startinsert
		  autocmd TermClose * ++once :q | call nvim_win_close(s:border_win, v:true)
		endfunction

	" Fonts change
		let s:fontsize = 15
		function! AdjustFontSize(amount)
		  let s:fontsize = s:fontsize+a:amount
		  :execute "GuiFont! Consolas:h" . s:fontsize
		endfunction
		noremap <C-ScrollWheelUp> :call AdjustFontSize(1)<CR>
		noremap <C-ScrollWheelDown> :call AdjustFontSize(-1)<CR>
		inoremap <C-ScrollWheelUp> <Esc>:call AdjustFontSize(1)<CR>a
		inoremap <C-ScrollWheelDown> <Esc>:call AdjustFontSize(-1)<CR>
