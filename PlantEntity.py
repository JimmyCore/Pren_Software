API_KEY = '2b10glUixSPZOunMJ952kc5Pe'
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


class Plant:
    def __init__(self, position: int, scientificNameWithoutAuthor, genus, family, scientificName, commonNames,
                 scientificNameWithoutAuthor_2=None, genus_2=None, family_2=None, scientificName_2=None,
                 commonNames_2=None):
        self.position = position
        self.scientificNameWithoutAuthor = scientificNameWithoutAuthor
        self.genus = genus
        self.family = family
        self.scientificName = scientificName
        self.commonNames: list = commonNames

        self.scientificNameWithoutAuthor_2 = scientificNameWithoutAuthor_2
        self.genus_2 = genus_2
        self.family_2 = family_2
        self.scientificName_2 = scientificName_2
        self.commonNames_2 = commonNames_2

    def has_two_scores(self):
        if self.scientificName_2 is None:
            return False
        else:
            return True

    def compare_family(self, plant):
        if plant is not None:
            if self.family.lower() == plant.family.lower():
                return True
            elif self.has_two_scores():
                if self.family_2.lower() == plant.family.lower():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def compare_scientificNameWithoutAuthor(self, plant):
        if plant is not None:
            if self.scientificNameWithoutAuthor.lower() == plant.scientificNameWithoutAuthor.lower():
                return True
            elif self.has_two_scores():
                if self.scientificNameWithoutAuthor_2.lower() == plant.scientificNameWithoutAuthor.lower():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def compare_genus(self, plant):
        if plant is not None:
            if self.genus.lower() == plant.genus.lower():
                return True
            elif self.has_two_scores():
                if self.genus_2.lower() == plant.genus.lower():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def compare_scientificName(self, plant):
        if plant is not None:
            if self.scientificName.lower() == plant.scientificName.lower():
                return True
            elif self.has_two_scores():
                if self.scientificName_2.lower() == plant.scientificName.lower():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def compare_commonNames(self, plant):
        if plant is not None:
            if len(set(self.commonNames).intersection(plant.commonNames)) > 0:
                return True
            elif self.has_two_scores():
                if len(set(self.commonNames_2).intersection(plant.commonNames)) > 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
