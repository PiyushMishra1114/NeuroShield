import pefile
import os
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
        pe = pefile.PE(file_path)

        entropy_list = []
        for section in pe.sections:
            entropy_list.append(get_entropy(section.get_data()))

        features = {
            "SizeOfCode": pe.OPTIONAL_HEADER.SizeOfCode,
            "SizeOfInitializedData": pe.OPTIONAL_HEADER.SizeOfInitializedData,
            "SizeOfUninitializedData": pe.OPTIONAL_HEADER.SizeOfUninitializedData,
            "AddressOfEntryPoint": pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            "BaseOfCode": pe.OPTIONAL_HEADER.BaseOfCode,
            "ImageBase": pe.OPTIONAL_HEADER.ImageBase,
            "SectionMaxEntropy": max(entropy_list) if entropy_list else 0,
            "SectionMinEntropy": min(entropy_list) if entropy_list else 0,
            "NumberOfSections": len(pe.sections),
            "DllCharacteristics": pe.OPTIONAL_HEADER.DllCharacteristics,
            "SizeOfStackReserve": pe.OPTIONAL_HEADER.SizeOfStackReserve,
            "SizeOfHeapReserve": pe.OPTIONAL_HEADER.SizeOfHeapReserve,
        }

        return features

    except Exception as e:
        print(f"[ERROR] Failed to process {file_path}: {e}")
        return None
