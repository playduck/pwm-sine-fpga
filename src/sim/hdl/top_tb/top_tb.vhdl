library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;

entity top_tb is
    -- this entity defines a testbench for the sine waveform generator module.
    -- the purpose of this testbench is to provide a clock input to the sine waveform generator module
    -- and to observe its output.
end top_tb;

architecture sim of top_tb is

    -- this constant defines the time period of the clock signal.
    constant CLK_PERIOD : time := 10 ns;

    -- these signals are declared to interface with the sine waveform generator module.
    signal clk : std_logic := '0';
    signal pwm : std_logic := '0';

    component top is
        port (
            clk_in  : in std_logic;
            pwm_out : out std_logic
        );
    end component;

begin

    -- the sine waveform generator module is instantiated here with the entity name UUT (Unit Under Test).
    UUT : top
    port map(
        clk_in  => clk,
        pwm_out => pwm
    );

    process
    begin
        wait for 10 ns;
        -- this process generates the clock signal that will be used to drive the sine waveform generator module.
        while now < 1 sec loop
            clk <= not clk;
            wait for CLK_PERIOD/2;
        end loop;
        wait;
    end process;

end sim;
