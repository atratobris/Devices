require 'faraday'
require 'nokogiri'

class Action
  PIN = 13
  PIN2 = 10
  ACTION = 0 # 0 = OFF | 1 = ON

  attr_accessor :board_ip, :pins


  def initialize
    # @board_ip = `arp -a | grep arduino`.split("(")[1].split(")")[0]
    @board_ip = '192.168.0.128'
    @pins = {}
    puts "Connecting to #{board_ip}.."
    run
  end

  private

  def run
    initial_value =  get_pin_value PIN2
    while initial_value == (get_pin_value PIN2)
      sleep 1
    end

    5.times do |i|
      # update_pin_values
      set_pin_value (i%2 == 0 ? 0 : 1)
      sleep 1
    end
  end

  def update_pin_values
    parse_body(Faraday.get "http://#{board_ip}/arduino/webserver")
    puts "Updated pin values.. Pin 13 is #{pins['13']}"
  end

  def set_pin_value value
    response = Faraday.get("http://#{board_ip}/arduino/digital/#{PIN}/#{value}") #rescue nil
    puts response.body
    # puts "Setting pin 13.."
  end

  def parse_body response
    document = Nokogiri::XML(response.body)
    document.css("pin").each do |pin|
      @pins[pin['number']] = pin.inner_text.to_i
    end
  end

  def get_pin_value pin
    response = Faraday.get("http://#{@board_ip}/arduino/digital/#{pin}")
    value = response.body
    puts "Pin #{PIN} = #{value}"
    return value.to_i
  end
end

Action.new
