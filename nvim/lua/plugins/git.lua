return {
  -- Git blame / diff decorations (gitsigns already in LazyVim, just enable extras)
  {
    "lewis6991/gitsigns.nvim",
    opts = {
      current_line_blame = true,
      current_line_blame_opts = {
        delay = 500,
      },
    },
  },
}
