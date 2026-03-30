return {
  -- Error lens: show diagnostics inline at end of line (usernamehw.errorlens equivalent)
  {
    "rachartier/tiny-inline-diagnostic.nvim",
    event = "LspAttach",
    opts = {
      preset = "simple",
    },
  },
}
