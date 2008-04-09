<TeXmacs|1.0.6.10>

<style|<tuple|source|scripts>>

<\body>
  <active*|<\src-title>
    <src-package|code-blocks|1.0>

    <\src-purpose>
      Code environments
    </src-purpose>

    <src-copyright|2004|Matteo Bertini>

    <\src-license>
      This <TeXmacs> style package falls under the <hlink|GNU general public
      license|$TEXMACS_PATH/LICENSE> and comes WITHOUT ANY WARRANTY
      WHATSOEVER. If you do not have a copy of the license, then write to the
      Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
      02111-1307, USA.
    </src-license>
  </src-title>>

  <\active*>
    <\src-comment>
      Fragments of code.
    </src-comment>
  </active*>

  <assign|scheme|<name|Scheme>>

  <assign|cpp|<name|C++>>

  <assign|c|<name|C>>

  <assign|ada|<samp|Ada>>

  <assign|py|<samp|Python>>

  <assign|pyx|<samp|Pyrex>>

  <assign|au|<samp|AUnit>>

  <assign|tg|<samp|tg>>

  <assign|ct|<samp|ctypes>>

  \;

  <assign|framed-fragment|<\macro|x|xcolor|xtitle>
    <\verbatim>
      <\with|par-par-sep|0.4fn|font-base-size|10|par-left|0fn>
        <\surround|<vspace*|0.5fn>|<vspace|0.5fn>>
          <tabular|<tformat|<cwith|2|2|1|1|cell-hyphen|t>|<twith|table-width|80spc>|<cwith|1|1|1|1|cell-background|grey>|<cwith|2|2|1|1|cell-background|<arg|xcolor>>|<cwith|2|2|1|1|cell-tborder|0.5ln>|<cwith|2|2|1|1|cell-bsep|0.5spc>|<cwith|1|2|1|1|cell-tsep|0.5spc>|<cwith|1|2|1|1|cell-bsep|0.5spc>|<cwith|2|2|1|1|cell-tsep|0.5spc>|<twith|table-lborder|0.5ln>|<twith|table-rborder|0.5ln>|<twith|table-bborder|0.5ln>|<twith|table-tborder|0.5ln>|<table|<row|<cell|<arg|xtitle>>>|<row|<\cell>
            <arg|x>
          </cell>>>>>
        </surround>
      </with>
    </verbatim>
  </macro>>

  <assign|c-fragment|<\macro|xtitle|x>
    <quote-env|<framed-fragment|<with|par-par-sep|0fn|<arg|x>>|pastel
    red|<arg|xtitle>>>
  </macro>>

  <assign|ada-fragment|<\macro|xtitle|x>
    <quote-env|<framed-fragment|<with|par-par-sep|0fn|<arg|x>>|pastel
    blue|<arg|xtitle>>>
  </macro>>

  <assign|py-fragment|<\macro|xtitle|x>
    <quote-env|<framed-fragment|<with|par-par-sep|0fn|<arg|x>>|pastel
    green|<arg|xtitle>>>
  </macro>>

  <assign|pyx-fragment|<\macro|xtitle|x>
    <quote-env|<framed-fragment|<with|par-par-sep|0fn|<arg|x>>|pastel
    green|<arg|xtitle>>>
  </macro>>

  <assign|sh-fragment|<\macro|xtitle|x>
    <quote-env|<framed-fragment|<with|par-par-sep|0fn|<arg|x>>|pastel
    yellow|<arg|xtitle>>>
  </macro>>

  <assign|citation|<\macro|name|uri|text>
    <\with|par-mode|center|par-par-sep|0.5fn>
      <\surround|<vspace*|0.5fn>|<vspace|0.5fn>>
        <tabular|<tformat|<twith|table-lborder|1px>|<cwith|2|2|1|1|cell-hyphen|t>|<twith|table-width|0.9par>|<table|<row|<cell|<with|font-series|bold|<arg|name>>:
        <hlink|<arg|uri>|<arg|uri>>>>|<row|<\cell>
          <with|font-shape|italic|<arg|text>>
        </cell>>>>>
      </surround>
    </with>
  </macro>>

  \;

  <assign|todo|<macro|x|<block|<tformat|<cwith|1|1|1|1|cell-background|pastel
  red>|<cwith|1|1|1|1|cell-lborder|0.5ln>|<cwith|1|1|1|1|cell-rborder|0.5ln>|<cwith|1|1|1|1|cell-bborder|0.5ln>|<cwith|1|1|1|1|cell-tborder|0.5ln>|<table|<row|<cell|To
  do: <arg|x>>>>>>>>

  <\active*>
    <\src-comment>
      Code colors.
    </src-comment>
  </active*>

  \;

  <assign|num|<macro|x|<with|color|dark red|<arg|x>>>>

  <assign|esc|<macro|x|<with|color|dark red|<arg|x>>>>

  <assign|dstr|<macro|x|<with|color|dark orange|<arg|x>>>>

  <assign|str|<macro|x|<with|color|dark orange|<arg|x>>>>

  <assign|slc|<macro|x|<with|font-shape|italic|<with|color|dark
  green|<arg|x>>>>>

  <assign|com|<macro|x|<with|font-shape|italic|<with|color|dark
  green|<arg|x>>>>>

  <assign|dir|<macro|x|<with|color|dark blue|<arg|x>>>>

  <assign|sym|<macro|x|<with|color|dark blue|<arg|x>>>>

  <assign|line|<macro|x|<with|color|dark blue|<arg|x>>>>

  <assign|kwa|<macro|x|<with|color|blue|<arg|x>>>>

  <assign|kwb|<macro|x|<with|color|dark red|<arg|x>>>>

  <assign|kwc|<macro|x|<with|font-series|bold|<with|color|dark
  blue|<arg|x>>>>>

  <assign|kwd|<macro|x|<with|font-series|bold|<arg|x>>>>

  \;
</body>

<\initial>
  <\collection>
    <associate|language|english>
    <associate|par-par-sep|0fn>
    <associate|preamble|true>
  </collection>
</initial>