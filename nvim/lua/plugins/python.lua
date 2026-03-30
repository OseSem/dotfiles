return {
  -- Point pyright at uv's .venv, and add ty (Astral's type checker)
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        pyright = {
          settings = {
            python = {
              venvPath = ".",
              venv = ".venv",
            },
          },
        },
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
