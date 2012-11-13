require 'sass'

module AssetFiles
  module Sass
    module Functions
      def static_path(source)
        ::Sass::Script::String.new File.join(django_static_url, source.value), :string
      end

      def static_url(source)
        ::Sass::Script::String.new "url(#{static_path(source)})"
      end

      protected

        def django_static_url
          @django_static_url ||= ENV['DJANGO_STATIC_URL'] || '..'
        end
    end
  end
end

module Sass::Script::Functions
  include AssetFiles::Sass::Functions

  declare :static_path, [:source]
  declare :static_url, [:source]
end
