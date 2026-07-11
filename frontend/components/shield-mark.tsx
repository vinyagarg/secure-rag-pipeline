import { Shield } from 'lucide-react'
import { cn } from '@/lib/utils'

export function ShieldMark({
  size = 16,
  className,
}: {
  size?: number
  className?: string
}) {
  return (
    <Shield
      size={size}
      strokeWidth={2}
      className={cn('text-foreground', className)}
      aria-hidden="true"
    />
  )
}
