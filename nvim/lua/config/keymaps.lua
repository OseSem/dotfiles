-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- Ctrl+Backspace deletes previous word in insert mode
vim.keymap.set("i", "<C-BS>", "<C-w>", { desc = "Delete word backwards" })
