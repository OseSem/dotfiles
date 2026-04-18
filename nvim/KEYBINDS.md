# Neovim Keybinds

Reference for this LazyVim setup. Leader key is `<Space>`.

> Press `<Space>` and pause — `which-key` shows every group interactively.
> `<leader>sk` fuzzy-searches **all** registered keymaps.

## Table of contents

- [Leader menu groups](#leader-menu-groups)
- [Window & buffer navigation](#window--buffer-navigation)
- [Jumping around code](#jumping-around-code)
- [LSP (code intelligence)](#lsp-code-intelligence)
- [File explorer (neo-tree)](#file-explorer-neo-tree)
- [Search / pickers (snacks)](#search--pickers-snacks)
- [Git](#git)
- [Editing](#editing)
- [Terminal](#terminal)
- [Diagnostics / Trouble](#diagnostics--trouble)
- [Copilot](#copilot)
- [Custom binds](#custom-binds)

---

## Leader menu groups

| Prefix | Group | Quick picks |
|---|---|---|
| `<leader><space>` | Find files (smart) | |
| `<leader>/` | Grep in cwd | |
| `<leader>,` | Switch buffer | |
| `<leader>:` | Command history | |
| `<leader>f` | **File / Find** | `ff` files · `fr` recent · `fg` grep · `fb` buffers · `fn` new file · `fc` config files |
| `<leader>s` | **Search** | `sg` grep · `sw` grep word · `sh` help · `sk` keymaps · `sd` diagnostics · `ss` symbols · `sr` resume last |
| `<leader>b` | **Buffer** | `bd` delete · `bo` close others · `bp` pin · `bP` close unpinned |
| `<leader>c` | **Code (LSP)** | `ca` action · `cr` rename · `cf` format · `cd` line diagnostic · `cs` symbols · `cl` LspInfo |
| `<leader>g` | **Git** | `gg` lazygit · `gb` blame line · `gB` blame file · `gL` log · `gf` file history |
| `<leader>u` | **UI toggle** | `uw` wrap · `us` spell · `un` number · `uc` conceal · `ub` background · `ur` clear highlights · `ud` diagnostics |
| `<leader>x` | **Diagnostics / Trouble** | `xx` all · `xX` buffer · `xl` loclist · `xq` quickfix |
| `<leader>w` | **Windows** | `ws` hsplit · `wv` vsplit · `wd` close · `ww` next |
| `<leader>q` | **Session / Quit** | `qq` quit all · `qs` restore session · `qd` don't save session |
| `<leader>l` | **Lazy** | `ll` Lazy UI · `lx` LazyExtras |
| `<leader>t` | **Terminal** | `tt` terminal · `tT` terminal in cwd |
| `<leader>n` | **Notifications** | `nd` dismiss all · `nh` history |
| `<leader>a` | **AI (Copilot)** | Copilot chat / toggles |

---

## Window & buffer navigation

| Keys | Action |
|---|---|
| `<C-h>` / `<C-j>` / `<C-k>` / `<C-l>` | Move between windows |
| `<C-Up>` / `<C-Down>` / `<C-Left>` / `<C-Right>` | Resize window |
| `<S-h>` / `<S-l>` | Previous / next buffer |
| `[b` / `]b` | Previous / next buffer |
| `<leader>bd` | Delete buffer |
| `<leader>ww` | Other window |
| `<leader>ws` / `<leader>wv` | Horizontal / vertical split |
| `<leader>wd` | Close window |

---

## Jumping around code

| Keys | Action |
|---|---|
| `gd` | Goto definition |
| `gD` | Goto declaration |
| `gr` | References |
| `gI` | Goto implementation |
| `gy` | Goto type definition |
| `K` | Hover docs |
| `gK` | Signature help |
| `[d` / `]d` | Previous / next diagnostic |
| `[e` / `]e` | Previous / next error |
| `[w` / `]w` | Previous / next warning |
| `[c` / `]c` | Previous / next git hunk |
| `[[` / `]]` | Previous / next function / class |
| `<C-o>` / `<C-i>` | Jump back / forward in jumplist |

---

## LSP (code intelligence)

| Keys | Action |
|---|---|
| `<leader>ca` | Code action |
| `<leader>cr` | Rename symbol |
| `<leader>cA` | Source action |
| `<leader>cf` | Format buffer |
| `<leader>cd` | Line diagnostics |
| `<leader>cs` | Document symbols |
| `<leader>cS` | Workspace symbols |
| `<leader>cl` | `:LspInfo` |
| `<leader>cm` | Mason |

---

## File explorer (neo-tree)

| Keys | Action |
|---|---|
| `<leader>e` / `<leader>fe` | Toggle neo-tree at project root |
| `<leader>E` / `<leader>fE` | Toggle neo-tree at cwd |
| `<leader>ge` | Git status explorer |
| `<leader>be` | Buffer explorer |

**Inside neo-tree:**

| Key | Action |
|---|---|
| `a` | Add file/directory (end path with `/` for dir) |
| `d` | Delete |
| `r` | Rename |
| `y` | Copy to clipboard |
| `x` | Cut |
| `p` | Paste |
| `c` | Copy (prompts for destination) |
| `m` | Move |
| `H` | Toggle hidden files |
| `/` | Fuzzy find inside tree |
| `f` | Filter |
| `<CR>` | Open |
| `s` / `S` | Open in vsplit / hsplit |
| `t` | Open in new tab |
| `q` | Close |
| `?` | Help |

---

## Search / pickers (snacks)

Top-level search entry points:

| Keys | Action |
|---|---|
| `<leader><space>` | Find files (smart) |
| `<leader>/` | Live grep |
| `<leader>ff` | Find files |
| `<leader>fg` | Grep |
| `<leader>fr` | Recent files |
| `<leader>fb` | Find buffers |
| `<leader>fc` | Find config files |
| `<leader>sw` | Grep word under cursor |
| `<leader>sk` | Search keymaps |
| `<leader>sh` | Search help |
| `<leader>sc` | Command history |
| `<leader>sd` | Diagnostics (workspace) |
| `<leader>sr` | Resume last picker |

**Inside a picker:**

| Key | Action |
|---|---|
| `<C-j>` / `<C-k>` | Next / previous result |
| `<CR>` | Open |
| `<C-v>` | Open in vsplit |
| `<C-x>` | Open in hsplit |
| `<C-t>` | Open in new tab |
| `<Tab>` | Multi-select |
| `<C-q>` | Send to quickfix |
| `?` | Show picker-specific keys |

---

## Git

| Keys | Action |
|---|---|
| `<leader>gg` | Lazygit (project root) |
| `<leader>gG` | Lazygit (cwd) |
| `<leader>gb` | Blame line |
| `<leader>gB` | Blame file (full) |
| `<leader>gL` | Git log |
| `<leader>gf` | File history |
| `<leader>gY` | Copy permalink to cursor line |
| `]c` / `[c` | Next / previous hunk |
| `<leader>ghs` | Stage hunk |
| `<leader>ghr` | Reset hunk |
| `<leader>ghp` | Preview hunk |
| `<leader>ghS` | Stage buffer |
| `<leader>ghR` | Reset buffer |
| `<leader>ghu` | Undo stage hunk |
| `<leader>ghd` | Diff this |

---

## Editing

| Keys | Action |
|---|---|
| `<C-s>` | Save |
| `<Esc>` | Clear search highlight |
| `<A-j>` / `<A-k>` | Move line / selection down / up |
| `<` / `>` (visual) | Indent / dedent (keeps selection) |
| `gcc` | Toggle line comment |
| `gc` (visual) | Toggle selection comment |
| `gco` / `gcO` | Add comment below / above |
| `ys{motion}{char}` | Surround add (e.g. `ysiw"` → wrap word in `"…"`) |
| `cs"'` | Change surrounding `"` to `'` |
| `ds"` | Delete surrounding `"` |
| `S"` (visual) | Surround selection with `"` |
| `*` / `#` | Search word under cursor forward / back |
| `<leader>-` | Split below |
| `<leader>\|` | Split right |

---

## Terminal

| Keys | Action |
|---|---|
| `<C-/>` or `<C-_>` | Toggle floating terminal |
| `<leader>tt` | Open terminal |
| `<leader>tT` | Open terminal in cwd |

**Inside terminal:**

| Key | Action |
|---|---|
| `<Esc><Esc>` | Exit insert mode (normal mode in term) |
| `<C-/>` | Close terminal |

---

## Diagnostics / Trouble

| Keys | Action |
|---|---|
| `<leader>xx` | All diagnostics |
| `<leader>xX` | Buffer diagnostics |
| `<leader>xs` | Symbols outline |
| `<leader>xL` | Location list |
| `<leader>xQ` | Quickfix list |
| `<leader>xt` | TODO comments |

---

## Copilot

| Keys | Action |
|---|---|
| `<A-]>` | Accept next suggestion |
| `<A-[>` | Previous suggestion |
| `<A-/>` | Dismiss |
| `<leader>aa` | Copilot chat toggle |
| `:Copilot` | Command menu |
| `:Copilot auth` | Authenticate |
| `:Copilot status` | Check status |

---

## Custom binds

From `lua/config/keymaps.lua`:

| Keys | Action |
|---|---|
| `<C-BS>` (insert mode) | Delete previous word |

---

## Cheat: how to learn more

- **`<Space>` then wait** — which-key popup groups everything.
- **`<leader>sk`** — fuzzy-search every keymap defined in this session.
- **`<leader>sh`** — search help docs.
- **`:map`** — list all active mappings (raw).
- **`:verbose nmap <keys>`** — show where a mapping was defined (great for debugging overrides).
