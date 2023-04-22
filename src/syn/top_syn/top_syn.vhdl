library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;

entity top_syn is
    port (
        clk_in  : in std_logic;         -- clk input
        pwm_out : out std_logic := '0'  -- sine modulated pwm output
    );
end top_syn;

architecture behavioral of top_syn is
    component top is
        generic (
            BIT_DEPTH     : natural := 16;
            SAMPLE_AMOUNT : natural := 64
        );
        port (
            clk_in  : in std_logic;
            pwm_out : out std_logic
        );
    end component;

    component pll0 is
        port (
            clkin : in std_logic;
            clkout0 : out std_logic;
            locked : out std_logic
        );
    end component;

    signal mclk : std_logic := '0';

begin
    clk_pll1:  pll0
    port map (
        clkin => clk_in,
        clkout0 => mclk,
        locked => open
    );

    top_inst: top
    port map(
        clk_in  => mclk,
        pwm_out => pwm_out
    );

end behavioral;
