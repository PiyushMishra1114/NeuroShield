import pefile
import math

def get_entropy(data):
    if not data:
        return 0.0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy -= p_x * math.log2(p_x)
    return entropy

def extract_features(file_path):
    try:
        pe = pefile.PE(file_path, fast_load=True)
        pe.parse_data_directories()

        entropy_list = []
        for section in pe.sections:
            try:
                data = section.get_data()
                entropy_list.append(get_entropy(data))
            except Exception:
                continue  # silently skip sections that can't be read

        features = {
            "SizeOfCode": getattr(pe.OPTIONAL_HEADER, "SizeOfCode", 0),
            "SizeOfInitializedData": getattr(pe.OPTIONAL_HEADER, "SizeOfInitializedData", 0),
            "SizeOfUninitializedData": getattr(pe.OPTIONAL_HEADER, "SizeOfUninitializedData", 0),
            "AddressOfEntryPoint": getattr(pe.OPTIONAL_HEADER, "AddressOfEntryPoint", 0),
            "BaseOfCode": getattr(pe.OPTIONAL_HEADER, "BaseOfCode", 0),
            "ImageBase": getattr(pe.OPTIONAL_HEADER, "ImageBase", 0),
            "SectionMaxEntropy": max(entropy_list) if entropy_list else 0,
            "SectionMinEntropy": min(entropy_list) if entropy_list else 0,
            "NumberOfSections": len(pe.sections),
            "DllCharacteristics": getattr(pe.OPTIONAL_HEADER, "DllCharacteristics", 0),
            "SizeOfStackReserve": getattr(pe.OPTIONAL_HEADER, "SizeOfStackReserve", 0),
            "SizeOfHeapReserve": getattr(pe.OPTIONAL_HEADER, "SizeOfHeapReserve", 0),
        }

        return features

    except pefile.PEFormatError:
        return None
    except Exception:
        return None
