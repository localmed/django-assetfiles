require 'sass'

module AssetFiles
  module Sass
    module Functions
      def static_path(source)
        ::Sass::Script::String.new File.join(django_static_url, source.value), :string
      end

      def static_url(source, only_path = nil, cache_buster = nil)
        if only_path == true || only_path.respond_to?(:value) && only_path.value == true
          return static_path(source)
        end

        ::Sass::Script::String.new "url(#{static_path(source)})"
      end

      alias :image_path :static_path
      alias :image_url :static_url
      alias :font_path :static_path
      alias :font_url :static_url

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
  declare :image_path, [:source]
  declare :image_url,  [:source]
  declare :image_url,  [:source, :only_path]
  declare :image_url,  [:source, :only_path, :cache_buster]
  declare :font_path,  [:source]
  declare :font_url,   [:source]
  declare :font_url,   [:source, :only_path]
end
