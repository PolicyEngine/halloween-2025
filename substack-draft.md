# Everything Is Software: How I Accidentally Pioneered TDD for Music Composition

Last weekend, I visited my college friend Ian in LA. Ian's both a software developer and musician, and over coffee he walked me through the current landscape of AI music tools.

"Suno can generate full songs from text prompts now," he explained, showing me examples on his phone. "Udio does studio-quality tracks. AIVA composes soundtracks for films."

The results were genuinely impressive. But as he demoed each tool—chat boxes, web interfaces, parameter sliders—something occurred to me.

"What about AI *coding agents*?" I asked. "Could you use Claude Code or Cursor to actually compose music? Like, write code that synthesizes audio?"

Ian paused. "Huh. I haven't seen anyone do that."

Neither had I. I did a quick mental search through GitHub projects, blog posts, demos I'd seen. AI music tools: plenty. AI coding agents used for music: nothing came to mind.

We moved on to other topics. I didn't think about it again until a few days later.

## The Accidental Experiment

Thursday night, I needed something fun for Halloween. PolicyEngine needed a festive social media post—nothing fancy, just a spooky version of our logo for Twitter.

"Can you make a Halloween-flavored version of our logo and maybe a social post?" I asked Claude Code.

It created orange and purple logo variants. Good. Then I got greedy.

"Make it more hardcore," I said, showing it a spooky AI-generated image. "And add a soundtrack."

I expected Claude to tell me to use Suno, or point me to some audio generation API. Instead, it wrote Python code:

```python
def generate_spooky_soundtrack(duration=6, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Deep droning bass
    bass = 0.3 * np.sin(2 * np.pi * 55 * t)

    # Eerie high-pitched whistle
    wind = 0.15 * np.sin(2 * np.pi * 800 * t)
    ...
```

Actual audio synthesis. NumPy arrays, sine waves, frequency modulation, ADSR envelopes. It was generating waveforms from scratch—writing code that creates audio.

"Can you improve it?" I asked, listening to the first version.

This is where it got interesting.

## The TDD Breakthrough

"Want me to use TDD?" Claude suggested. "I can create quality tests for the soundtrack and iteratively improve it."

Test-driven development. For music composition. I'd never heard of such a thing.

Within seconds, it had written `test_soundtrack_quality.py`—a comprehensive audio analyzer that measures:

- **Frequency coverage:** Sub-bass (20-60Hz), bass (60-250Hz), mids, highs
- **Dynamic range:** Crest factor in dB (not too flat, not too sparse)
- **Activity distribution:** Percentage of time with meaningful sound
- **Spectral variety:** How much the timbre changes over time
- **Pacing:** Whether events are distributed evenly throughout

It ran the tests on the first soundtrack:

```
Overall Score: 1/5 tests passed
Status: FAIL

✗ FREQUENCY_COVERAGE
  ✗ has_sub_bass (4.17%, need 15%+)
  ✗ has_bass (10.09%, need 20%+)

IMPROVEMENT SUGGESTIONS:
- Add more sub-bass content (20-60Hz) for visceral impact
```

Then Claude went to work.

It increased bass amplitudes. Added more low frequencies. Applied EQ filters to separate frequency ranges. Re-ran the tests.

**Iteration 2:** 3/5 tests passed (sub-bass up to 11.9%)
**Iteration 4:** 4/5 tests passed (sub-bass: 15.3% ✓, bass: 18.7%)
**Iteration 6:** 4/5 tests passed (bass: 19.5%, pacing failing)
**Iteration 8:** 5/5 tests passed ✓

Final metrics:
- Sub-bass: 18.2% ✓
- Bass: 30.7% ✓
- Dynamic range: 12.7dB ✓
- Spectral variety: High ✓
- Event pacing: [4,1,2] evenly distributed ✓

I sat back and stared at my screen. This wasn't AI making music. This was AI doing software engineering *on* music.

## Why Nobody's Done This

After the fact, I did the research I should have done over coffee with Ian. Here's the current landscape:

**AI Music Tools (All Interface-Based):**
- **Suno, Udio:** Text-to-music generation. Type "epic Halloween soundtrack" → get MP3
- **AIVA, Beatoven, Mubert:** Soundtrack composition through web interfaces
- **MuseCoco:** Microsoft's symbolic music copilot (still generates MIDI/symbolic)
- **Mozart AI, Riff:** "Cursor for music production"—but they're DAW interfaces, not coding agents

**AI Coding Agents:**
- **GitHub Copilot, Cursor, Devin, Windsurf, Aider, Claude Code**
- Used for: Writing functions, debugging, refactoring, deploying apps
- Used for music composition: *crickets*

I found one developer who used Claude Code to port a music teaching app. Another who generated white noise (just `np.random.randn()`). Someone integrated Sonic Pi for playback. But nobody had used an AI coding agent to synthesize original multi-layered music and systematically optimize it.

The tools exist in parallel universes. Music AI lives in slick interfaces. Coding AI lives in terminals and text editors. Never the twain shall meet.

Except... why not?

## The Core Insight

Here's what clicked: **Everything that can be expressed as code can be improved through software engineering feedback loops.**

Compare these two workflows:

**Traditional AI Music Tools:**
1. Prompt: "Make a spooky Halloween soundtrack"
2. Get result
3. Prompt again: "Make it spookier"
4. Get new result
5. Repeat until satisfied (or give up)

The AI doesn't learn from iteration to iteration. It doesn't measure whether "spookier" worked. It just generates something different and hopes you like it better.

**Code-Based Music with TDD:**
1. Define quality criteria: "Sub-bass should be 15%+ of frequency energy"
2. Generate music through code (sine waves, envelopes, filters)
3. Run objective tests: "Sub-bass is 4.17% ✗"
4. Make targeted fix: Increase bass amplitudes, add low frequencies
5. Re-test: "Sub-bass is 11.9%"
6. Iterate with precise feedback until: "Sub-bass is 18.2% ✓"

The difference isn't just methodology. It's *transparency*. When music is code, you can measure it, test it, and systematically improve it within a single session.

## The Technique: Four-Layer Composition with EQ

The final soundtrack has:

**Bass Layer (`generate_bass_layer.py`):**
- 12 sub-bass frequencies (20-60Hz)
- 15 bass frequencies (60-250Hz)
- Thunder rumbles with full low-end spectrum
- Kept at 0.95 amplitude (near-maximum)

**Melody Layer (`generate_melody_layer.py`):**
- Church bell tolls with inharmonic partials
- Descending music box melody (dissonant minor scale)
- Ghostly theremin frequency sweeps
- High-pass filtered at 300Hz before mixing (to avoid bass clash)

**Atmosphere Layer (`generate_atmosphere_layer.py`):**
- Dissonant choir (ghostly sustained chords)
- Dark ambient pad
- Ethereal high shimmer
- Also high-pass filtered at 300Hz

**Effects Layer (`generate_effects_layer.py`):**
- Multi-layered wind
- Creaking wood with noise texture
- Bat wing swooshes (frequency sweeps)
- Footsteps building tension
- Rattling chains
- Distant howls
- Also high-pass filtered at 300Hz

**Mixing (`mix_soundtrack.py`):**
```python
# Bass layer gets ALL the low end
mixed = (
    1.00 * bass +              # Full volume, untouched
    0.06 * melody_filtered +   # Almost silent, no bass
    0.07 * atmosphere_filtered +
    0.08 * effects_filtered
)

# Apply 3:1 compression at 0.3 threshold
# Final result passes all 5 quality tests
```

Each layer is generated independently, then mixed with careful EQ separation. The bass layer owns everything below 300Hz. Everything else stays above 300Hz. This prevents frequency masking and ensures the sub-bass test passes.

## The Broader Implication

We tend to think of AI music tools and AI coding tools as separate categories. But they're not. One is just more advanced in recognizing that **creative output, when expressed as code, becomes subject to software engineering methodologies**.

What else could work this way?

- **Graphic design:** SVG generation with TDD for composition, color theory, visual balance
- **Video editing:** Programmatic timeline manipulation with quality metrics
- **Writing:** Structured text generation with readability, coherence, and style tests
- **Game design:** Procedural generation with playability, difficulty, and engagement metrics

The pattern is: *If you can express it in code, you can test it. If you can test it, you can improve it systematically.*

## What We Built

The final result: [policyengine.github.io/halloween-2025](https://policyengine.github.io/halloween-2025/)

A spooky PolicyEngine logo with:
- Floating ghosts, flying bats, jack-o-lanterns
- Custom SVG animations
- A 12-second cinematic soundtrack with:
  - 4 separate layers (bass, melody, atmosphere, effects)
  - Church bells, ghostly choir, howling wind, thunder
  - Creaking wood, footsteps, chains, bat swooshes
  - All generated from sine waves and noise
  - All optimized through TDD

The soundtrack passes five objective quality tests. The code is on GitHub. Anyone can run the tests, modify the parameters, regenerate the audio, and verify it still meets quality standards.

## The Future

AI coding agents are getting better at *everything*, not just code. But we're still thinking of them in narrow terms—"code assistants" for writing functions and fixing bugs.

The real opportunity: **Applying software engineering principles to creative domains by expressing creative output as code.**

Not "use AI to make music." But "use AI to write code that makes music, then use software engineering to systematically improve it."

The difference is profound. One is a black box that gets better through scale and training data. The other is a transparent, measurable, improvable system that gets better through feedback loops *within your session*.

Everything is software. And AI coding agents are just beginning to understand that.

---

*The Halloween project, including all soundtrack generation code, quality tests, and TDD iterations, is open source at [github.com/PolicyEngine/halloween-2025](https://github.com/PolicyEngine/halloween-2025). Happy Halloween! 🎃*
