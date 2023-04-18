library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;

entity top is
    generic (
        BIT_DEPTH     : natural := 16;
        SAMPLE_AMOUNT : natural := 256
    );
    port (
        clk_in  : in std_logic;         -- clk input
        pwm_out : out std_logic := '0'  -- sine modulated pwm output
    );
end top;

architecture behavioral of top is

    signal sine_out : std_logic_vector(BIT_DEPTH - 1 downto 0) := (others => '0');
    signal sync_out : std_logic                                := '0';

    component sine_wave_generator is
        generic (
            BIT_DEPTH     : natural := BIT_DEPTH;
            SAMPLE_AMOUNT : natural := SAMPLE_AMOUNT
        );
        port (
            clk      : in std_logic;                                -- Clock input
            sine_out : out std_logic_vector(BIT_DEPTH - 1 downto 0) -- Sine wave output
        );
    end component;

    component pwm_generator is
        generic (
            BIT_DEPTH : natural := BIT_DEPTH
        );
        port (
            clk         : in std_logic;
            pulse_width : in std_logic_vector(BIT_DEPTH - 1 downto 0);
            pwm_out     : out std_logic;
            sync_out    : out std_logic
        );
    end component;

    -- component epll is
    --     port (
    --         clkin : in std_logic;
    --         clkout0 : out std_logic;
    --         locked : out std_logic
    --     );
    -- end component;

begin

    -- sine wave generator is clocked by the 50% pulse of the pwm generator
    -- each pwm generation thus generates a new sine wave sample
    SWG : sine_wave_generator
    port map(
        clk      => sync_out,
        sine_out => sine_out
    );

    -- pulse width is modulated by the sine wave
    PWM : pwm_generator
    port map(
        clk         => clk_in,
        pulse_width => sine_out,
        pwm_out     => pwm_out,
        sync_out    => sync_out
    );

end behavioral;
