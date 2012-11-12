require 'sass'

module AssetFiles
  module Sass
    module Functions
      def asset_path(source)
        ::Sass::Script::String.new File.join(static_url, source.value), :string
      end

      def asset_url(source)
        ::Sass::Script::String.new "url(#{asset_path(source)})"
      end

      protected

        def static_url
          @static_url ||= ENV['DJANGO_STATIC_URL'] || '..'
        end
    end
  end
end

module Sass::Script::Functions
  include AssetFiles::Sass::Functions

  declare :asset_path, [:source]
  declare :asset_url, [:source]
end
