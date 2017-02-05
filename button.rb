require 'faraday'
require 'nokogiri'

class Button
  PIN = 13

  def initialize
    @board_ip = '192.168.0.128'
    run
  end

  private
  def run
    puts "started run "
    # get pin value
    value = get_pin_value PIN

    # set the opposite value
    newValue = (value+1)%2
    puts "new value : #{newValue}"
    set_pin_value newValue
  end

  def set_pin_value value
    response = Faraday.get("http://#{@board_ip}/arduino/digital/#{PIN}/#{value}") #rescue nil
    value = response.body
    puts "Pin #{PIN} set to #{value}"
  end

  def get_pin_value pin
    response = Faraday.get("http://#{@board_ip}/arduino/digital/#{pin}")
    value = response.body
    puts "Pin #{PIN} = #{value}"
    return value.to_i
  end
end

Button.new
