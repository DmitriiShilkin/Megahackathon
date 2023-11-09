from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Post, Category, Comment, Like


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = Category
        fields = [
            'name',
        ]
        # отключаем встроенный валидатор, чтобы не было ошибки уникальности имен,
        # т.к. при создании публикации мы не создаем новые категории, а берем имеющиеся
        # extra_kwargs = {
        #     'name': {
        #         'validators': []
        #     },
        # }

    def save(self, **kwargs):
        self.is_valid()
        name = self.validated_data.get('name')
        category = Category.objects.filter(name=name)
        if category.exists():
            return category.first()

    # def create(self, validated_data):
    #     pass

    # def validate_name(self, value):
    #     category = Category.objects.filter(name=value)
    #     if not category.exists():
    #         raise serializers.ValidationError(f'Указано имя несуществующей категории {value}')
    #
    #     return value

    # def get_choices(self, request):
    #     queryset = Category.objects.all()
    #     choices = {}
    #     for q in queryset:
    #         choices[q] = q
    #     return choices


# сериализатор модели публикаций
class PostSerializer(WritableNestedModelSerializer):
    # category = serializers.ManyRelatedField(child_relation=CategorySerializer())
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    category = CategorySerializer(many=True, required=True)
    image = serializers.URLField(label='URL', allow_blank=True)

    class Meta:
        model = Post
        depth = 1
        fields = [
            'id',
            'text',
            'image',
            'category',
        ]

    # проверяем имя переданной категории, преобразуем OrderedDict с именами категорий в список объектов типа "Категория"
    # и возвращаем его
    def validate_category(self, value):
        categories = []

        if value:
            for val in value:
                # достаем имя каждой категории из OrderedDict
                category_name = list(val.items())[0][1]
                # проверяем есть ли категория с указанным именем
                category = Category.objects.filter(name=category_name).first()

                if not category:
                    raise serializers.ValidationError(f"Указано имя несуществующей категории '{category_name}'")

                categories.append(category)

            return categories

    # переопредяем метод post
    def create(self, validated_data, **kwargs):
        # получаем данные публикации из валидатора
        categories = validated_data.pop('category')
        user = validated_data.pop('user')
        text = validated_data.pop('text')
        image = validated_data.pop('image')
        # создаем публикацию
        post = Post.objects.create(text=text, image=image, author=user)
        # добавляем связи с категориями
        if categories:
            post.category.set(categories)

        return post
