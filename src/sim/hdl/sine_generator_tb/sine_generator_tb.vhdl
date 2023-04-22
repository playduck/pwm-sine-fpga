library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;

entity sine_generator_tb is
end sine_generator_tb;

architecture sim of sine_generator_tb is

    -- this constant defines the time period of the clock signal.
    constant CLK_PERIOD : time := 10 ns;

    -- these signals are declared to interface with the sine waveform generator module.
    signal clk : std_logic := '0';

    component sine_wave_generator is
        generic (
            BIT_DEPTH     : natural := 8;
            SAMPLE_AMOUNT : natural := 16
        );
        port (
            clk      : in std_logic;                                -- clock input
            sine_out : out std_logic_vector(BIT_DEPTH - 1 downto 0) := (others => '0') -- sine wave output
        );
    end component;

begin

    UUT : sine_wave_generator
    port map(
        clk  => clk
    );

    process
    begin
        wait for 10 ns;
        while now < 1 sec loop
            clk <= not clk;
            wait for CLK_PERIOD/2;
        end loop;
        wait;
    end process;

end sim;
