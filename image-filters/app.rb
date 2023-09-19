require 'sinatra'
require 'rmagick'
require 'open-uri'
require 'base64'
include Magick

$filters = ['sketch', 'solarize', 'blur_image', 'charcoal', 'motion_blur', 'negate', 'oil_paint', 'polaroid', 'sepiatone', 'segment']

def make_page(selected='negate', url='https://thecatapi.com/api/images/get?format=src&type=jpeg')
  index = '<form action=/ method=POST>Image url: <input style="width:50em" type=text name=url value="%s"><br>Filter: <select name=filter>' % url
  for filter in $filters
    index += '<option value=%s>%s</option>' % [selected == filter ? filter + ' selected' : filter, filter]
  end
  index += '</select><br><input type=submit value="Apply filter"></form><br><br>'
  index
end

class App < Sinatra::Base
  get '/' do
    make_page
  end

  post '/' do
    url = params[:url]
    filter = params[:filter]
    if !$filters.include?(filter)
      return make_page + 'Bad filter'
    end
    img = Image.from_blob(URI.open(url, :read_timeout => 5).read).first
    img.format = 'jpeg'
    img = img.send(filter)
    data_uri = Base64.encode64(img.to_blob).gsub(/\n/, "") 
    make_page(filter, url) + '<img src="data:image/jpeg;base64,%s">' % data_uri
  end
end