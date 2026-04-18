-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua

-- Save all buffers when focus leaves Neovim (VSCode "onFocusChange" behavior).
-- Pairs with vim.opt.autowrite, which only saves when switching buffers inside Neovim.
vim.api.nvim_create_autocmd("FocusLost", {
  group = vim.api.nvim_create_augroup("save_on_focus_lost", { clear = true }),
  pattern = "*",
  command = "silent! wall",
})
