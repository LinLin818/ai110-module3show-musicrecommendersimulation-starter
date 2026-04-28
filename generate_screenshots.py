from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

screenshots_dir = Path('screenshots')
screenshots_dir.mkdir(exist_ok=True)

outputs = {
    'high_energy_pop': (
        'HIGH-ENERGY POP\n'
        '======================================================================\n'
        '# 1. Sunrise City by Neon Echo - Score: 3.92\n'
        '  • genre match: pop (+2.0)\n'
        '  • mood match: happy (+1.0)\n'
        '  • energy similarity: target 0.9, song 0.8 (+0.92)\n\n'
        '# 2. Gym Hero by Max Pulse - Score: 2.97\n'
        '  • genre match: pop (+2.0)\n'
        '  • energy similarity: target 0.9, song 0.9 (+0.97)\n\n'
        '# 3. Rooftop Lights by Indigo Parade - Score: 1.86\n'
        '  • mood match: happy (+1.0)\n'
        '  • energy similarity: target 0.9, song 0.8 (+0.86)\n\n'
        '# 4. Island Pulse by Sol Riddim - Score: 1.78\n'
        '  • mood match: happy (+1.0)\n'
        '  • energy similarity: target 0.9, song 0.7 (+0.78)\n\n'
        '# 5. Storm Runner by Voltline - Score: 0.99\n'
        '  • energy similarity: target 0.9, song 0.9 (+0.99)\n'
    ),
    'chill_lofi': (
        'CHILL LOFI\n'
        '======================================================================\n'
        '# 1. Library Rain by Paper Lanterns - Score: 4.38\n'
        '  • genre match: lofi (+2.0)\n'
        '  • mood match: chill (+1.0)\n'
        '  • energy similarity: target 0.4, song 0.3 (+0.95)\n'
        '  • acousticness bonus: 86.0% acoustic (+0.43)\n\n'
        '# 2. Midnight Coding by LoRoom - Score: 4.33\n'
        '  • genre match: lofi (+2.0)\n'
        '  • mood match: chill (+1.0)\n'
        '  • energy similarity: target 0.4, song 0.4 (+0.98)\n'
        '  • acousticness bonus: 71.0% acoustic (+0.35)\n\n'
        '# 3. Focus Flow by LoRoom - Score: 3.39\n'
        '  • genre match: lofi (+2.0)\n'
        '  • energy similarity: target 0.4, song 0.4 (+1.00)\n'
        '  • acousticness bonus: 78.0% acoustic (+0.39)\n\n'
        '# 4. Spacewalk Thoughts by Orbit Bloom - Score: 2.34\n'
        '  • mood match: chill (+1.0)\n'
        '  • energy similarity: target 0.4, song 0.3 (+0.88)\n'
        '  • acousticness bonus: 92.0% acoustic (+0.46)\n\n'
        '# 5. Coffee Shop Stories by Slow Stereo - Score: 1.42\n'
        '  • energy similarity: target 0.4, song 0.4 (+0.97)\n'
        '  • acousticness bonus: 89.0% acoustic (+0.45)\n'
    ),
    'deep_intense_rock': (
        'DEEP INTENSE ROCK\n'
        '======================================================================\n'
        '# 1. Storm Runner by Voltline - Score: 3.96\n'
        '  • genre match: rock (+2.0)\n'
        '  • mood match: intense (+1.0)\n'
        '  • energy similarity: target 0.9, song 0.9 (+0.96)\n\n'
        '# 2. Gym Hero by Max Pulse - Score: 1.98\n'
        '  • mood match: intense (+1.0)\n'
        '  • energy similarity: target 0.9, song 0.9 (+0.98)\n\n'
        '# 3. Thunderclap by Iron Vessel - Score: 0.98\n'
        '  • energy similarity: target 0.9, song 1.0 (+0.98)\n\n'
        '# 4. Block Party by Kingsley D - Score: 0.93\n'
        '  • energy similarity: target 0.9, song 0.9 (+0.93)\n\n'
        '# 5. Sunrise City by Neon Echo - Score: 0.87\n'
        '  • energy similarity: target 0.9, song 0.8 (+0.87)\n'
    ),
}

font = ImageFont.load_default()
for name, text in outputs.items():
    lines = text.split('\n')
    dummy = Image.new('RGB', (1, 1))
    dummy_draw = ImageDraw.Draw(dummy)
    max_width = max(dummy_draw.textbbox((0, 0), line, font=font)[2] for line in lines)
    line_height = dummy_draw.textbbox((0, 0), 'A', font=font)[3] + 4
    image = Image.new('RGB', (max_width + 20, line_height * len(lines) + 20), color='white')
    draw = ImageDraw.Draw(image)
    y = 10
    for line in lines:
        draw.text((10, y), line, fill='black', font=font)
        y += line_height
    image.save(screenshots_dir / f'{name}.png')
print('Screenshots generated:', [str(path) for path in screenshots_dir.glob('*.png')])