return {
  -- Use ty (Astral's Python type checker) instead of pyright.
  -- The switch itself is done via vim.g.lazyvim_python_lsp in config/options.lua.
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        ty = {},
      },
    },
  },

  -- Format with ruff on save
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        python = { "ruff_format", "ruff_fix" },
      },
    },
  },
}
