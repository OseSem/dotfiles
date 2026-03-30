return {
  -- Catppuccin Macchiato (matches VSCode theme)
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    opts = {
      flavour = "macchiato",
      integrations = {
        gitsigns = true,
        neo_tree = true,
        mason = true,
        telescope = { enabled = true },
        which_key = true,
        treesitter = true,
        notify = true,
      },
    },
  },
  {
    "LazyVim/LazyVim",
    opts = { colorscheme = "catppuccin" },
  },
}
