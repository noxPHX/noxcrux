from rest_framework.serializers import Serializer, CharField, ValidationError


class TOTPSerializer(Serializer):

    totp_code = CharField(max_length=6, write_only=True, required=True)

    def validate_totp_code(self, value):
        if not self.instance:
            raise ValidationError("You have not setup two factor authentication.")
        if not self.instance.verify_token(value):
            raise ValidationError("Invalid TOTP Token.")
        return value

    def update(self, instance, validated_data):
        if instance.confirmed:
            raise ValidationError("You already have confirmed your device.")
        instance.confirmed = True
        instance.save()
        return instance

    def create(self, validated_data):
        pass
