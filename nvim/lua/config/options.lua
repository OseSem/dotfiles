-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

vim.opt.autowrite = true -- auto-save on window change (matches VSCode files.autoSave)

-- Use ty (Astral's type checker) instead of pyright. The LazyVim python extra
-- reads this variable to decide which Python LSP to enable; any value other
-- than "pyright"/"basedpyright" disables both.
vim.g.lazyvim_python_lsp = "ty"
