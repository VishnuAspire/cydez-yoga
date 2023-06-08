from rest_framework import serializers
from . models import program,banner,Category,Level,order

class orderSerializer(serializers.ModelSerializer):
	class Meta:
		model=order
		fields='__all__'

class catgorySerializer(serializers.ModelSerializer):
	# category=serializers.CharField(source='category.name',allow_blank=True,allow_null=True)
	class Meta:
		model=Category
		fields='__all__'
			
	

class levelSerializer(serializers.ModelSerializer):
	class Meta:
		model=Level
		fields='__all__'

class programSerializer(serializers.ModelSerializer):
	# category=catgorySerializer(many=True)
	# level=levelSerializer(many=True)
	class Meta:
		model=program
		fields=[
				'id',
				'title',
				'price',
				'minimumregisterprice',
				'numberofactivedays',
				'numberofclass',
				'style',
				'category',
				'level',
				'introduction',
				'video_url',
				'image'
		]
		
class programSerializer1(serializers.ModelSerializer):
	# category=catgorySerializer(many=True)
	# level=levelSerializer(many=True)

		class Meta:
		
			model=program
			fields=[
					'id',
					'title',
					'price',
					'minimumregisterprice',
					'numberofactivedays',
					'numberofclass',
					'style',
					'category',
					'level',
					'introduction',
					'image'
			]
	
class slideSerializer(serializers.ModelSerializer):
	class Meta:
		model=banner
		fields='__all__'
