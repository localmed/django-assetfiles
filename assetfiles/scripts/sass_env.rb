# This is a custom Sass binstub to create a Bundle-aware Sass command.
# This is different from using `bundle exec` because it actually requires all
# of the gems in Gemfile, instead of just setting up a sandbox. This is
# necessary so required gems can potentially add to the Sass load path
# before running the command.

begin
  require 'bundler'
rescue LoadError
else
  Bundler.require if Bundler::SharedHelpers.in_bundle?
end
