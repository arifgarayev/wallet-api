from typing import Any, List, Dict


class CommonUtils:

    @staticmethod
    def model_update(
        instance: Any,
        fields: List[str],
        data: Dict[str, Any],
    ):
        has_updated = False

        for field in fields:
            if field not in data:
                continue

            if getattr(instance, field) != data[field]:
                has_updated = True
                setattr(instance, field, data[field])

        if has_updated:
            instance.full_clean()
            instance.save(update_fields=fields)

        return instance, has_updated
