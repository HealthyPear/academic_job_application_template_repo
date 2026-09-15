import argparse
import bibtexparser
import yaml
import re

# Mapping of common journal abbreviations to full names
JOURNAL_ABBREVIATIONS = {
    "\\apj": "The Astrophysical Journal",
    "\\apjl": "The Astrophysical Journal Letters",
    "\\memsai": "Memorie della Societa Astronomica Italiana",
    "\\mnras": "Monthly Notices of the Royal Astronomical Society",
    "\\aap": "Astronomy & Astrophysics",
    "\\aj": "The Astronomical Journal",
    "\\nat": "Nature",
    "\\science": "Science",
    "\\prd": "Physical Review D",
    "\\prl": "Physical Review Letters",
}

MONTH_MAPPING = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


def remove_curly_braces(text):
    return re.sub(r"[{}]", "", text)

def parse_bibtex(file_path):
    bib_database = bibtexparser.parse_file(file_path)
    return bib_database.entries

def get_field(entry, key, default=None):
    """Get the string value of a bibtexparser v2 Field, or a default."""
    field = entry.get(key)
    if field is None:
        return default
    return field.value

def format_authors(authors, user_name, max_authors):
    author_list = [
        remove_curly_braces(author.strip()) for author in authors.split(" and ")
    ]
    author_list = [
        f"***{author}***" if author == user_name else author for author in author_list
    ]

    if len(author_list) > max_authors:
        return [author_list[0], "et al."]

    if "Collaboration" in author_list[-1]:
        author_list[-1] = f"on behalf of {author_list[-1]}"

    return author_list


def convert_entry(entry, user_name, max_authors):
    yaml_entry = {
        "title": remove_curly_braces(get_field(entry, "title", "Unknown Title")),
        "authors": format_authors(
            get_field(entry, "author", "Unknown Author"), user_name, max_authors
        ),
    }

    doi = get_field(entry, "doi")
    if doi:
        yaml_entry["doi"] = remove_curly_braces(doi)

    url = get_field(entry, "url")
    if url:
        yaml_entry["url"] = remove_curly_braces(url)

    journal = get_field(entry, "journal")
    if journal:
        journal = remove_curly_braces(journal).strip()
        yaml_entry["journal"] = JOURNAL_ABBREVIATIONS.get(journal, journal)

    year = get_field(entry, "year")
    if year:
        date = remove_curly_braces(year)
        month = get_field(entry, "month")
        if month:
            month = remove_curly_braces(month).lower()[:3]
            date += f"-{MONTH_MAPPING.get(month, month)}"
        day = get_field(entry, "day")
        if day:
            date += f"-{remove_curly_braces(day).zfill(2)}"
        yaml_entry["date"] = date

    return yaml_entry


def convert_bib_to_yaml(input_file, output_file, user_name, max_authors, sort_order):
    entries = parse_bibtex(input_file)
    yaml_entries = [convert_entry(entry, user_name, max_authors) for entry in entries]

    yaml_entries.sort(
        key=lambda x: x.get("date", "0000"), reverse=(sort_order == "desc")
    )

    with open(output_file, "w", encoding="utf-8") as yaml_file:
        yaml.dump(yaml_entries, yaml_file, allow_unicode=True, sort_keys=False)
    print(f"Converted {len(entries)} entries to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a .bib file to RenderCV YAML format."
    )
    parser.add_argument("input", help="Path to the input .bib file")
    parser.add_argument("output", help="Path to the output YAML file")
    parser.add_argument(
        "--user-name", required=True, help="Your name to be bolded in the author list"
    )
    parser.add_argument(
        "--max-authors",
        type=int,
        default=5,
        help="Maximum number of authors before using 'et al.'",
    )
    parser.add_argument(
        "--sort",
        choices=["asc", "desc"],
        default="desc",
        help="Sort entries by date (asc or desc)",
    )
    args = parser.parse_args()

    convert_bib_to_yaml(
        args.input, args.output, args.user_name, args.max_authors, args.sort
    )


if __name__ == "__main__":
    main()
