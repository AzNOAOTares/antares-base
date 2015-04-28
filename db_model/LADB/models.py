from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Image( models.Model ):
    """
    The class corresponds to the 'Image' table.
    """
    ImageID = models.IntegerField( primary_key=True )    
    TakenAt = models.DateTimeField( 'Time the image was taken' )
    TelescopeName = models.CharField( max_length=100 )
    FilterPassband = models.CharField( max_length=500 )
    
    def __str__( self ):
        return "Image {0} taken at {1} by telescope {2}".format(
            self.ImageID, self.TakenAt, self.TelescopeName )

class Locus( models.Model ):
    """
    The class corresponds to the 'Locus' table.
    """
    LocusID = models.IntegerField( primary_key=True )
    Coordinate = models.CharField( max_length=500 )
    Uncertainty = models.IntegerField()

    def __str__( self ):
        return "Locus {0} at {1} with uncertainty of {2}".format(
            self.LocusID, self.Coordinate, self.Uncertainty )

class LocusAggregatedAlert( models.Model ):
    """
    The class corresponds to the 'LocusAggregatedAlert' table.
    """
    LAAID = models.IntegerField( primary_key=True )
    LocusID = models.ForeignKey( Locus )
    
class Source( models.Model ):
    """
    The class corresponds to the 'Source' table.
    """
    SourceID = models.IntegerField( primary_key=True )
    ImageID = models.ForeignKey( Image )
    Coordinate = models.CharField( max_length=500 )
    Brightness = models.FloatField()
    DeltaBrightness = models.FloatField()
    ThumbnailURL = models.URLField()

    def __str__( self ):
        return "Source {0} from image {1}".format( self.SourceID, self.ImageID )

class Alert( models.Model ):
    """
    The class corresponds to the 'Alert' table.
    """
    decisions = (
        ( 'NA', 'Not Applicable' ),
        ( 'T', 'Throttled Alert' ),
        ( 'D', 'Diverted immediately' ),
        ( 'L1', 'Level-I Alert' ),
        ( 'L2', 'Level-II Alert' ),
        ( 'R', 'Rarest of the rare Alert' ),
    )

    AlertID = models.IntegerField( primary_key=True )
    TakenAt = models.DateTimeField( 'Time the alert was taken' )
    LocusID = models.ForeignKey( Locus )
    SourceID = models.ForeignKey( Source )
    Decision = models.CharField( max_length=50, choices=decisions, default='NA' )
    # LAAID = models.ForeignKey( LocusAggregatedAlert )

    def __str__( self ):
        return "Alert {0}: {1}".format( self.AlertID, self.Decision )

    def is_throttled( self ):
        return self.Decision == 'T'

    def is_dirverted_immediately( self ):
        return self.Decision == 'D'

    def is_level_1_alert( self ):
        return self.Decision == 'L1'

    def is_level_1_alert( self ):
        return self.Decision == 'L2'

    def is_rarest_of_the_rare( self ):
        return self.Decision == 'R'

class AlertReplica( models.Model ):
    """
    The class corresponds to the 'AlertReplica' table.
    """
    ReplicaID = models.IntegerField( primary_key=True )
    AlertID = models.ForeignKey( Alert )
    # put a >0 constraint on ReplicaNumber field
    ReplicaNumber = models.IntegerField( validators=[MinValueValidator(1)] )
    LocusID = models.ForeignKey( Locus )
    ChannelID = models.IntegerField()
    ChannelProbability = models.FloatField()

    def __str__( self ):
        return "Alert replica {0} of alert {1}".format( self.ReplicaNumber, self.AlertID )

class AstroObject( models.Model ):
    """
    The class corresponds to the 'AlertReplica' table.
    """
    AstroObjectID = models.IntegerField( primary_key=True )
    LocusID = models.ForeignKey( Locus )
    Catalog = models.CharField( max_length=500 )
    IDinCatalog = models.IntegerField()
    IsPointSource = models.BooleanField( default=False )

    def __str__( self ):
        return "Astro object {0} from catalog {1}".format(
            self.AstroObjectID, self.Catalog )

class Attribute( models.Model ):
    """
    The class corresponds to the 'Attribute' table.
    """
    AttrName = models.CharField( max_length=100, primary_key=True )
    IsScaled = models.BooleanField( default=False )
    DataType = models.CharField( max_length=500 )

    def __str__( self ):
        return "Attribute {0}".format(self.AttrName)

class AttributeValue( models.Model ):
    """
    The class corresponds to the 'AttributeValue' table.
    """
    # List of choices of type a container can be
    container_types = (
        ( 'A', 'AstroObject Table' ),
        ( 'C', 'Combo Table' ),
        ( 'I', 'Image Table' ),
        ( 'E', 'Alert Table' ),
        ( 'L', 'LocusAggregatedAlert Table' ),
        ( 'M', 'ImageSection Table' ),
        ( 'R', 'AlertReplica Table' ),
        ( 'S', 'Source Table' ),
    )

    AttributeValueID = models.IntegerField( primary_key=True )
    AttrName = models.ForeignKey( Attribute )
    ContainerID = models.IntegerField()
    ContainerType = models.CharField( max_length=1, choices=container_types )
    ComputedAt = models.DateTimeField( 'Time the value was computed' )
    # For now, just use a string to store value.
    Value = models.CharField( max_length=500 )
    Annotation = models.CharField( max_length=500 )
    Confidence = models.FloatField()

    def __str__( self ):
        return self.Annotation

    class Meta:
        unique_together = ( 'AttrName', 'ContainerID',
                            'ContainerType', 'ComputedAt' )

class DerivedAttribute( models.Model ):
    """
    The class corresponds to the 'DerivedAttribute' table.
    """
    AttrName = models.ForeignKey( Attribute )
    HashName = models.CharField( max_length=40 )
    FunctionName = models.CharField( max_length=50 )
    FileName = models.CharField( max_length=50 )
    PackageName = models.CharField( max_length=50 )
    AstronomerName = models.CharField( max_length=50 )

class ReplicaAssociatedWith( models.Model ):
    """
    The class corresponds to the 'ReplicaAssociatedWith' table.
    """
    ReplicaID = models.ForeignKey( AlertReplica )
    AstroObjectID = models.ForeignKey( AstroObject )
    AssociationProbability = models.FloatField()


