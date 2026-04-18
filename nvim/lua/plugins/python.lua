return {
  -- Use ty (Astral's Python type checker) instead of pyright / basedpyright.
  -- The LazyVim python extra is steered by vim.g.lazyvim_python_lsp (set in
  -- config/options.lua). The explicit enabled=false below is belt-and-suspenders
  -- in case that internal mechanism changes upstream.
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        ty = {},
        pyright = { enabled = false },
        basedpyright = { enabled = false },
      },
    },
  },

  -- Register ruff as the Python formatter for conform.nvim.
  -- Format-on-save is enabled by LazyVim default (toggle with <leader>uf).
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        python = { "ruff_format", "ruff_fix" },
      },
    },
  },
}
