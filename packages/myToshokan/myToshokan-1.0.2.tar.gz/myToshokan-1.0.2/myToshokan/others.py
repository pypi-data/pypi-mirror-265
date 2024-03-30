def remove_duplicate_languages(data):
    for i, item in enumerate(data, start=1):
        seen_languages = set()
        subtitles = item["Subtitles"]
        unique_subtitles = []

        for subtitle in subtitles:
            if subtitle["language"] not in seen_languages:
                seen_languages.add(subtitle["language"])
                unique_subtitles.append(subtitle)

        item["Subtitles"] = unique_subtitles
        print(f"Doublons supprimés : {i} / {len(data)}")