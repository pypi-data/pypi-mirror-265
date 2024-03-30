import re

def clean_script(script):
  pattern = re.compile(r"\[.*?\]|\(.*?\)")
  for item in script:
      item["text"] = re.sub(pattern, "", item["text"]).strip()

  pattern_start_to_end = re.compile(r"[\[\(].*")
  for item in script:
      item["text"] = re.sub(pattern_start_to_end, "", item["text"]).strip()

  pattern_any_to_end = re.compile(r".*[\]\)]")
  for item in script:
      item["text"] = re.sub(pattern_any_to_end, "", item["text"]).strip()

  ## delete the music symbol -> to do: delete all the symbols which can be interphered in the text analysis
  music_symbol_pattern = re.compile(r"♪")
  for item in script:
      item["text"] = re.sub(music_symbol_pattern, "", item["text"]).strip()

  # ## Delete the double dashes
  doubleDashes = re.compile(r"--")
  for item in script:
      item["text"] = re.sub(doubleDashes, "", item["text"]).strip()

  # ## Replace " -" by " "
  space_and_dash_pattern = re.compile(r" -+")
  for item in script:
      item["text"] = re.sub(space_and_dash_pattern, " ", item["text"]).strip()

  ## remplacer la boucle par une boucle for
  concacted_script = ""
  i = 0
  n = max([item['presentation_order'] for item in script])
  while i < n:
      concacted_script += script[i]['text'] + " "
      i += 1

  concacted_script = concacted_script.replace(" -", " ")

  return script